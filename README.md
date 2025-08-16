# 🏛️ ClauseWise - Legal Document Analyzer

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![IBM Granite](https://img.shields.io/badge/AI-IBM%20Granite%203.3-blue.svg)](https://ollama.ai)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**ClauseWise** is a powerful AI-driven legal document analyzer that transforms complex legal documents into easy-to-understand insights. Built with IBM's Granite 3.3:2B language model, it provides intelligent clause analysis, entity extraction, and interactive AI assistance for legal professionals and anyone working with legal documents.

## ✨ Key Features

### 🤖 **AI-Powered Analysis**
- **IBM Granite 3.3:2B Integration**: Leverages cutting-edge AI for accurate legal document understanding
- **Document Classification**: Automatically identifies document types (NDA, Employment Agreement, etc.)
- **Smart Clause Segmentation**: Intelligently breaks documents into analyzable sections

### 🔍 **Advanced Entity Recognition**
- **Parties & Organizations**: Identifies all legal entities, companies, and individuals
- **Financial Information**: Extracts monetary values, payment terms, and financial obligations
- **Critical Dates**: Finds deadlines, effective dates, and important timestamps
- **Contact Information**: Captures email addresses and phone numbers
- **Legal Obligations**: Highlights duties, responsibilities, and requirements
- **Legal Terms**: Identifies and explains complex legal terminology

### 💬 **Interactive AI Assistant**
- **Document Q&A**: Ask specific questions about your legal document
- **Risk Assessment**: Get insights on potential risks and liabilities
- **Plain English Translation**: Complex clauses simplified into understandable language
- **Context-Aware Responses**: AI maintains conversation history for better assistance

### 📄 **Multi-Format Support**
- **PDF Documents**: Full text extraction with formatting preservation
- **Word Documents (.docx)**: Complete document structure analysis
- **Text Files**: Direct text input and analysis
- **Copy-Paste Interface**: Quick analysis without file uploads

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Ollama** (for running local AI models)
- **Git**

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/clausewise.git
cd clausewise
```

2. **Install Ollama**
```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows - Download from https://ollama.ai
```

3. **Start Ollama service**
```bash
ollama serve
```

4. **Run ClauseWise**
```bash
python run.py
```

The startup script will automatically:
- Install Python dependencies
- Download the IBM Granite 3.3:2B model
- Create necessary directories
- Launch the web application at `http://localhost:5000`

### Manual Setup (Alternative)

If you prefer manual installation:

```bash
# Install dependencies
pip install -r requirements.txt

# Download the AI model
ollama pull granite3.3:2b

# Create directories
mkdir -p templates temp_uploads

# Start the application
python app.py
```

## 🎯 Usage

### 1. **Upload Your Document**
- **File Upload**: Drag and drop or browse for PDF, DOCX, or TXT files
- **Direct Input**: Copy and paste document text directly into the interface
- **Size Limit**: Up to 16MB per file

### 2. **Analyze Results**
Navigate through three comprehensive analysis views:

#### **📊 Entities Tab**
- View extracted legal entities in organized categories
- Click on any entity group for detailed AI explanations
- Visual metrics showing document complexity

#### **📋 Clauses Tab**
- Individual clause breakdown with smart segmentation
- **Simplify Button**: Get plain English explanations of complex clauses
- **Ask AI Button**: Query specific clauses for detailed analysis

#### **📄 Raw Text Tab**
- Complete document text with formatting preserved
- Searchable and copyable content

### 3. **Interactive AI Chat**
- Ask questions about document contents and implications
- Get risk assessments and legal guidance
- Use suggested questions for common legal inquiries
- Maintain conversation context for follow-up questions

## 📁 Project Structure

```
clausewise/
├── run.py                 # Smart startup script with dependency management
├── app.py                 # Main Flask application with AI integration
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html         # Base template with modern UI components
│   ├── index.html        # Upload interface with dual input methods
│   └── results.html      # Analysis results with interactive features
├── temp_uploads/         # Temporary file storage (auto-created)
└── README.md            # This file
```

## 🛠️ Technical Architecture

### **Backend Components**

**Flask Application (`app.py`)**
- Document processing pipeline with multi-format support
- RESTful API endpoints for AI interactions
- Advanced NLP for entity recognition using regex patterns
- Secure file handling with automatic cleanup

**AI Integration**
- **Model**: IBM Granite 3.3:2B via Ollama
- **Features**: Document classification, clause simplification, interactive chat
- **Performance**: Optimized for real-time responses
- **Scalability**: Configurable model parameters and hosting options

**Document Processing**
- **PDF**: `pdfplumber` for accurate text extraction
- **DOCX**: `python-docx` for Word document processing  
- **TXT**: UTF-8 text handling with error resilience
- **Clause Segmentation**: Intelligent parsing using legal document patterns

### **Frontend Components**

**Modern UI (`base.html`)**
- Responsive design with mobile-first approach
- Custom CSS with gradient themes and animations
- Modal dialogs for enhanced user experience
- Accessibility features with proper contrast and semantics

**Analysis Interface (`results.html`)**
- Three-panel layout for comprehensive document review
- Interactive entity visualization with hover effects
- Collapsible clause sections for focused analysis
- Real-time AI chat with typing indicators

**Upload Interface (`index.html`)**
- Dual input methods (file upload + text input)
- Drag-and-drop functionality with visual feedback
- File validation and progress indicators
- Usage tips and feature explanations

## ⚙️ Configuration

### **Default Settings**

```python
DEFAULT_SETTINGS = {
    'ollama_host': 'http://localhost:11434',
    'model_name': 'granite3.3:2b',
    'max_tokens': 512,
    'temperature': 0.2
}
```

### **Environment Variables** (Optional)

```bash
export CLAUSEWISE_MODEL="granite3.3:2b"
export CLAUSEWISE_HOST="http://localhost:11434"
export CLAUSEWISE_MAX_TOKENS="1024"
export CLAUSEWISE_TEMPERATURE="0.1"
```

### **File Limits**

- **Maximum file size**: 16MB
- **Supported formats**: PDF, DOCX, TXT
- **Concurrent uploads**: 1 per session
- **Processing timeout**: 120 seconds

## 🔧 Advanced Features

### **Custom Model Integration**

ClauseWise supports any Ollama-compatible model:

```bash
# Download alternative models
ollama pull llama2:70b
ollama pull mistral:7b
ollama pull codellama:34b

# Update model in app.py
DEFAULT_SETTINGS['model_name'] = 'llama2:70b'
```

### **API Endpoints**

- `POST /upload` - Document analysis endpoint
- `POST /simplify_clause` - Clause simplification API
- `POST /chat_document` - Interactive AI chat API

### **Extended Entity Recognition**

Current entity patterns support:
- **Dates**: Multiple formats (MM/DD/YYYY, Month Day, Year, etc.)
- **Money**: USD, INR, EUR, GBP with proper formatting
- **Contacts**: Email addresses and international phone numbers
- **Legal Terms**: 50+ common legal concepts and terminology
- **Parties**: Organization types, roles, and relationship identifiers

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Add tests** (if applicable)
5. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### **Development Setup**

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run with debug mode
export FLASK_ENV=development
python app.py
```

## 📋 Requirements

### **Python Dependencies**

```txt
flask>=2.0.0
requests>=2.28.0
werkzeug>=2.0.0
python-docx>=0.8.11
pdfplumber>=0.7.0
```

### **System Requirements**

- **OS**: Windows 10+, macOS 10.15+, Linux (Ubuntu 20.04+)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB for model + document storage
- **Network**: Internet connection for initial model download

## 🚨 Troubleshooting

### **Common Issues**

**1. Ollama Connection Error**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if not running
ollama serve
```

**2. Model Not Found**
```bash
# List available models
ollama list

# Download Granite model
ollama pull granite3.3:2b
```

**3. File Upload Errors**
- Check file size (max 16MB)
- Verify file format (PDF, DOCX, TXT only)
- Ensure file is not corrupted

**4. Python Dependencies**
```bash
# Reinstall requirements
pip install --upgrade -r requirements.txt

# Clear pip cache if needed
pip cache purge
```

### **Debug Mode**

Enable debug mode for detailed error information:

```bash
export FLASK_DEBUG=1
python app.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **IBM Granite Team** - For the exceptional language model
- **Ollama Project** - For the seamless local AI runtime
- **Flask Community** - For the robust web framework
- **Legal Tech Community** - For inspiration and feedback

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/clausewise/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/clausewise/discussions)
- **Email**: support@clausewise.com

---

**Built with ❤️ for the legal community**

*Making legal documents accessible to everyone through the power of AI*
