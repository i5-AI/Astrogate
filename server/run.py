#!/usr/bin/env python3
"""
Simple runner script for Astrogate backend
This handles virtual environment activation and startup
"""

import os
import sys
import subprocess

def main():
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("🔧 Activating virtual environment...")
        
        # Try to activate the virtual environment
        venv_path = os.path.join(os.path.dirname(__file__), 'chatbot')
        if os.path.exists(venv_path):
            # Add the virtual environment's bin directory to PATH
            venv_bin = os.path.join(venv_path, 'bin')
            if os.path.exists(venv_bin):
                os.environ['PATH'] = venv_bin + os.pathsep + os.environ['PATH']
                os.environ['VIRTUAL_ENV'] = venv_path
                sys.prefix = venv_path
                print(f"✅ Virtual environment activated: {venv_path}")
            else:
                print("❌ Virtual environment bin directory not found")
                return 1
        else:
            print("❌ Virtual environment not found. Please run: python3 -m venv chatbot")
            return 1
    
    # Import and run the app
    try:
        from app import app
        print("🚀 Starting Astrogate Air Force Chatbot...")
        print("✅ Backend ready! Frontend can now connect.")
        print("🌐 Access the chatbot at: http://localhost:5173")
        app.run(host="0.0.0.0", port=8000, debug=False)
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 