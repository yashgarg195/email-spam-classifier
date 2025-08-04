#!/usr/bin/env python3
"""
Setup script for the Email Spam Classifier
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("🚀 Setting up Email Spam Classifier...")
    print("=" * 50)
    
    # Check if Python 3 is available
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version} detected")
    
    # Install pip requirements
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Download spaCy model
    if not run_command("python -m spacy download en_core_web_sm", "Downloading spaCy English model"):
        print("❌ Failed to download spaCy model")
        sys.exit(1)
    
    # Create necessary directories
    print("📁 Creating directories...")
    os.makedirs('models', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    print("✅ Directories created")
    
    # Train the model
    print("\n🤖 Training the spam classifier...")
    if not run_command("python train_model.py", "Training the model"):
        print("❌ Failed to train the model")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("=" * 50)
    print("To run the application:")
    print("  python app.py")
    print("Then open your browser to: http://localhost:5000")
    print("\nHappy spam filtering! 🛡️")

if __name__ == "__main__":
    main() 