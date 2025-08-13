#!/usr/bin/env python3
"""
ClauseWise - Legal Document Analyzer Startup Script
"""
import subprocess
import sys
import time
import requests
import webbrowser
from pathlib import Path

def check_ollama_running():
    """Check if Ollama is running"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        return response.status_code == 200
    except:
        return False

def check_model_available(model_name="granite3.3:2b"):
    """Check if the specified model is available"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            return any(model['name'].startswith(model_name) for model in models)
        return False
    except:
        return False

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def setup_ollama():
    """Setup Ollama if needed"""
    print("\n🤖 Checking Ollama setup...")
    
    if not check_ollama_running():
        print("❌ Ollama is not running!")
        print("\n📋 To start Ollama:")
        print("   1. Install Ollama from https://ollama.ai")
        print("   2. Run: ollama serve")
        print("   3. Run this script again")
        return False
    
    print("✅ Ollama is running!")
    
    # Check for recommended model
    if not check_model_available():
        print("\n📥 Recommended model 'granite3.3:2b' not found.")
        response = input("Would you like to download it now? (y/n): ")
        if response.lower() == 'y':
            print("Downloading granite3.3:2b (this may take a few minutes)...")
            try:
                subprocess.run(['ollama', 'pull', 'granite3.3:2b'], check=True)
                print("✅ Model downloaded successfully!")
            except subprocess.CalledProcessError:
                print("❌ Failed to download model. You can download it manually with:")
                print("   ollama pull granite3.3:2b")
                return False
        else:
            print("⚠️  You can download it later with: ollama pull granite3.3:2b")
    else:
        print("✅ Model 'granite3.3:2b' is available!")
    
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['templates', 'temp_uploads']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("📁 Directories created/verified")

def start_application():
    """Start the Flask application"""
    print("\n🚀 Starting ClauseWise...")
    print("📱 The application will open in your browser automatically")
    print("🌐 Manual access: http://localhost:5000")
    print("\n💡 Tips:")
    print("   - Upload PDF, DOCX, or TXT legal documents")
    print("   - Use the AI chat to ask questions about your document")
    print("   - Click 'Simplify' on clauses for plain English explanations")
    print("\n" + "="*50)
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(2)
        webbrowser.open('http://localhost:5000')
    
    import threading
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start Flask app
    try:
        from app import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 ClauseWise stopped. Thank you for using our legal document analyzer!")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")

def main():
    """Main startup function"""
    print("=" * 50)
    print("🏛️  ClauseWise - Legal Document Analyzer")
    print("=" * 50)
    
    # Check if app.py exists
    if not Path('app.py').exists():
        print("❌ app.py not found! Make sure you're in the correct directory.")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements. Please run manually:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Setup Ollama
    if not setup_ollama():
        print("\n❌ Ollama setup incomplete. Please fix the issues above and try again.")
        sys.exit(1)
    
    # Start application
    start_application()

if __name__ == '__main__':
    main()