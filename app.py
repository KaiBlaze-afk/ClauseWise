from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
import re
import io
from typing import List, Dict, Any, Tuple
import requests
from werkzeug.utils import secure_filename
import json

# Optional dependencies
try:
    import docx
except ImportError:
    docx = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'temp_uploads'

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Default settings
DEFAULT_SETTINGS = {
    'ollama_host': 'http://localhost:11434',
    'model_name': 'granite3.3:2b',
    'max_tokens': 512,
    'temperature': 0.2
}

# File processing functions
def read_txt(file_bytes: bytes) -> str:
    return file_bytes.decode('utf-8', errors='ignore')

def read_docx(file_bytes: bytes) -> str:
    if docx is None:
        raise RuntimeError("python-docx not installed. Please install: pip install python-docx")
    file_like = io.BytesIO(file_bytes)
    d = docx.Document(file_like)
    return "\n".join(p.text for p in d.paragraphs)

def read_pdf(file_bytes: bytes) -> str:
    if pdfplumber is None:
        raise RuntimeError("pdfplumber not installed. Please install: pip install pdfplumber")
    text = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)

def extract_text(file_path: str) -> Tuple[str, str]:
    """Return (text, ext)"""
    name = file_path.lower()
    with open(file_path, 'rb') as f:
        data = f.read()
    
    if name.endswith(".txt"):
        return read_txt(data), "txt"
    elif name.endswith(".docx"):
        return read_docx(data), "docx"
    elif name.endswith(".pdf"):
        return read_pdf(data), "pdf"
    else:
        # fallback: try to decode as text
        return read_txt(data), "txt"

# Clause splitting regex patterns
CLAUSE_HEADING_RE = re.compile(r'^\s*(section|clause|article)\s+[\divx\.]+|^[A-Z][A-Z \-]{5,}$', re.IGNORECASE|re.MULTILINE)
CLAUSE_NUMBERED_RE = re.compile(r'^\s*(\d+(\.\d+)*|[ivx]+\.)\s+', re.IGNORECASE|re.MULTILINE)

def split_clauses(text: str) -> List[str]:
    # Normalize whitespace
    text_norm = re.sub(r'\r', '', text)
    # Insert markers before headings/numbered starts
    text_marked = CLAUSE_HEADING_RE.sub(lambda m: "\n<<<SPLIT>>>\n" + m.group(0), text_norm)
    text_marked = CLAUSE_NUMBERED_RE.sub(lambda m: "\n<<<SPLIT>>>\n" + m.group(0), text_marked)
    parts = [p.strip() for p in text_marked.split("<<<SPLIT>>>") if p.strip()]
    
    # Merge tiny fragments into neighbors
    merged = []
    for p in parts:
        if merged and (len(p) < 120):
            merged[-1] = merged[-1] + " " + p
        else:
            merged.append(p)
    
    # Fallback: if too few clauses, split by double newlines
    if len(merged) < 3:
        merged = [c.strip() for c in re.split(r'\n{2,}', text_norm) if c.strip()]
    
    return merged

# Enhanced NER patterns
DATE_RE = re.compile(r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4})\b', re.IGNORECASE)
MONEY_RE = re.compile(r'\b(?:USD|INR|\$|₹|€|GBP|£)\s?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?\b')
EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
PHONE_RE = re.compile(r'\+?\d[\d \-\(\)]{7,}\d')
PARTY_RE = re.compile(r'\b(?:Company|Employer|Employee|Disclosing Party|Receiving Party|Licensor|Licensee|Client|Contractor|Consultant|Corporation|LLC|Ltd|Inc|Partnership|Vendor|Supplier|Customer)\b', re.IGNORECASE)
OBLIGATION_RE = re.compile(r'\b(?:shall|must|will|agrees to|required to|obligated to|responsible for|duty to|covenant to)\b[^.]{0,100}', re.IGNORECASE)
LEGAL_TERM_RE = re.compile(r'\b(?:confidential|proprietary|intellectual property|copyright|trademark|patent|liability|indemnify|breach|terminate|default|force majeure|arbitration|jurisdiction|governing law)\b', re.IGNORECASE)

def enhanced_ner(text: str) -> Dict[str, List[str]]:
    ents = {
        "dates": sorted(set(DATE_RE.findall(text))),
        "monetary_values": sorted(set(MONEY_RE.findall(text))),
        "emails": sorted(set(EMAIL_RE.findall(text))),
        "phones": sorted(set(PHONE_RE.findall(text))),
        "parties": sorted(set(PARTY_RE.findall(text))),
        "obligations": sorted(set([match.strip() for match in OBLIGATION_RE.findall(text)])),
        "legal_terms": sorted(set(LEGAL_TERM_RE.findall(text))),
    }
    return ents

# Ollama integration
def ollama_chat(system: str, user: str, settings: dict) -> str:
    try:
        url = f"{settings['ollama_host']}/api/chat"
        payload = {
            "model": settings['model_name'],
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False,
            "options": {
                "temperature": float(settings['temperature']), 
                "num_predict": int(settings['max_tokens'])
            },
        }
        resp = requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data.get("message", {}).get("content", "").strip()
    except Exception as e:
        return f"[Ollama error] {str(e)}"

def classify_document(text: str, settings: dict) -> str:
    labels = [
        "Non-Disclosure Agreement (NDA)", 
        "Lease Agreement", 
        "Employment Agreement",
        "Service Agreement", 
        "Vendor Contract", 
        "Partnership Agreement",
        "License Agreement",
        "Purchase Agreement",
        "Other"
    ]
    system = "You are a precise legal document classifier. Respond with exactly one label from the provided options."
    prompt = f"Classify this document into one of these categories: {', '.join(labels)}.\n\nDocument excerpt:\n{text[:4000]}"
    result = ollama_chat(system, prompt, settings)
    
    # Find matching label
    for label in labels:
        if label.lower() in result.lower():
            return label
    return result[:100]

def simplify_clause(clause: str, settings: dict) -> str:
    system = """You are an expert legal translator who converts complex legal language into clear, simple English. 
    Your goal is to make legal concepts accessible to non-lawyers while preserving the original meaning and intent.
    Use simple words, shorter sentences, and explain any necessary legal concepts in plain language."""
    
    prompt = f"""Please rewrite the following legal clause in simple, easy-to-understand English:

Original clause:
\"\"\"{clause}\"\"\"

Simplified version:"""
    
    return ollama_chat(system, prompt, settings)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if we have either a file or text input
    document_text = request.form.get('document_text', '').strip()
    has_text = len(document_text) > 0
    
    file = request.files.get('file')
    has_file = file and file.filename != ''
    
    if not has_file and not has_text:
        flash('Please either upload a file or enter document text', 'error')
        return redirect(url_for('index'))
    
    try:
        # Get settings from form (using defaults for now)
        settings = DEFAULT_SETTINGS.copy()
        
        # Process based on input type
        if has_text:
            # Direct text input
            raw_text = document_text
            filename = "Direct Text Input"
            
        else:
            # File upload
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            try:
                # Extract text from file
                raw_text, ext = extract_text(file_path)
            finally:
                # Always clean up temp file
                if os.path.exists(file_path):
                    os.remove(file_path)
        
        # Validate that we have some text content
        if not raw_text or len(raw_text.strip()) < 10:
            flash('Document appears to be empty or too short to analyze', 'error')
            return redirect(url_for('index'))
        
        # Classify document
        doc_type = classify_document(raw_text, settings)
        
        # Extract entities
        entities = enhanced_ner(raw_text)
        
        # Split into clauses
        clauses = split_clauses(raw_text)
        
        return render_template('results.html', 
                             filename=filename,
                             doc_type=doc_type,
                             entities=entities,
                             clauses=clauses,
                             raw_text=raw_text,
                             settings=settings)
        
    except Exception as e:
        # Clean up temp file on error if it was created
        if has_file and 'file_path' in locals():
            if os.path.exists(file_path):
                os.remove(file_path)
        flash(f'Error processing document: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/simplify_clause', methods=['POST'])
def simplify_clause_route():
    data = request.get_json()
    clause = data.get('clause', '')
    settings = data.get('settings', DEFAULT_SETTINGS)
    
    if not clause:
        return jsonify({'error': 'No clause provided'}), 400
    
    try:
        simplified = simplify_clause(clause, settings)
        return jsonify({'simplified': simplified})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat_document', methods=['POST'])
def chat_document():
    data = request.get_json()
    message = data.get('message', '')
    document_context = data.get('document_context', '')
    chat_history = data.get('chat_history', [])
    settings = data.get('settings', DEFAULT_SETTINGS)
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        response = chat_with_document(message, document_context, chat_history, settings)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def chat_with_document(message: str, document_context: str, chat_history: list, settings: dict) -> str:
    """Chat with the document using context and history"""
    system_prompt = """You are a legal AI assistant specializing in document analysis and legal advice. 
    You have been provided with a legal document and can answer questions about its contents, implications, 
    and provide general legal guidance. 
    
    Key guidelines:
    - Base your answers on the provided document context
    - Provide clear, actionable advice when possible
    - Explain legal concepts in simple terms
    - Suggest practical next steps when appropriate
    - If asked about something not in the document, clearly state that
    - Always remind users to consult with a qualified attorney for specific legal advice
    - Be helpful but professional in tone"""
    
    # Build conversation context
    conversation_context = f"Document Content:\n{document_context[:3000]}\n\n"
    
    if chat_history:
        conversation_context += "Previous conversation:\n"
        for item in chat_history[-5:]:  # Last 5 exchanges
            conversation_context += f"User: {item.get('user', '')}\nAssistant: {item.get('assistant', '')}\n\n"
    
    conversation_context += f"Current question: {message}"
    
    return ollama_chat(system_prompt, conversation_context, settings)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)