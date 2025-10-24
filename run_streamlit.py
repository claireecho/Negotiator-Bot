#!/usr/bin/env python3
"""
Streamlit launcher for Negotiator Bot vs Recruiter Bot
"""

import subprocess
import sys
import os

def main():
    # Check if streamlit is installed
    try:
        import streamlit
    except ImportError:
        print("Streamlit not found. Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_streamlit.txt"])
    
    # Run streamlit app
    os.system("streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0")

if __name__ == "__main__":
    main()
