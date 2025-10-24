#!/usr/bin/env python3
"""
Demo script for the Streamlit Negotiator Bot vs Recruiter Bot application
"""

import webbrowser
import time
import subprocess
import sys
import os

def main():
    print("🤖 Negotiator Bot vs Recruiter Bot - Streamlit Demo")
    print("=" * 60)
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit is installed")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        print("✅ Streamlit installed successfully")
    
    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("❌ main.py not found. Please ensure you're in the correct directory.")
        return
    
    print("✅ main.py found")
    
    # Start the Streamlit app
    print("\n🚀 Starting Streamlit application...")
    print("📱 The app will open in your browser at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("\n" + "=" * 60)
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped. Thanks for using the Negotiator Bot!")
    except Exception as e:
        print(f"\n❌ Error running application: {e}")

if __name__ == "__main__":
    main()
