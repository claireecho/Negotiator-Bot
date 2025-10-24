#!/usr/bin/env python3
"""
Python 3.13 Compatible Installation Script
Handles Pillow and other package compatibility issues
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 13:
        print("✅ Python 3.13+ detected - using compatible package versions")
        return True
    elif version.major == 3 and version.minor >= 8:
        print("✅ Python 3.8+ detected - using standard package versions")
        return False
    else:
        print("❌ Python 3.8+ required")
        return False

def install_system_dependencies():
    """Install system dependencies based on OS"""
    system = platform.system().lower()
    
    if system == "linux":
        print("🐧 Linux detected - installing system dependencies")
        commands = [
            "sudo apt-get update",
            "sudo apt-get install -y python3-dev python3-venv",
            "sudo apt-get install -y libjpeg-dev zlib1g-dev"
        ]
        for cmd in commands:
            if not run_command(cmd, f"Running: {cmd}"):
                print(f"⚠️  Warning: {cmd} failed - you may need to install dependencies manually")
    
    elif system == "darwin":  # macOS
        print("🍎 macOS detected - checking for Xcode tools")
        run_command("xcode-select --install", "Installing Xcode command line tools")
    
    elif system == "windows":
        print("🪟 Windows detected - please ensure Visual Studio Build Tools are installed")
        print("Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/")

def install_python_packages():
    """Install Python packages with Python 3.13 compatibility"""
    print("📦 Installing Python packages...")
    
    # Upgrade pip and setuptools first
    upgrade_commands = [
        "pip install --upgrade pip",
        "pip install --upgrade setuptools wheel"
    ]
    
    for cmd in upgrade_commands:
        run_command(cmd, f"Running: {cmd}")
    
    # Install packages in order of dependency
    packages = [
        "Pillow>=12.0.0",  # Install Pillow first
        "reportlab>=4.4.4",  # Then reportlab
        "streamlit>=1.28.0",
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "Flask>=2.3.3",
        "gunicorn>=21.2.0",
        "httpx>=0.24.1"
    ]
    
    for package in packages:
        cmd = f"pip install --no-cache-dir {package}"
        if not run_command(cmd, f"Installing {package}"):
            print(f"⚠️  Warning: Failed to install {package}")

def verify_installation():
    """Verify that all packages are installed correctly"""
    print("🔍 Verifying installation...")
    
    test_imports = [
        ("streamlit", "Streamlit"),
        ("openai", "OpenAI"),
        ("PIL", "Pillow"),
        ("reportlab", "ReportLab"),
        ("flask", "Flask"),
        ("gunicorn", "Gunicorn"),
        ("httpx", "HTTPX"),
        ("dotenv", "python-dotenv")
    ]
    
    all_good = True
    for module, name in test_imports:
        try:
            __import__(module)
            print(f"✅ {name} - OK")
        except ImportError as e:
            print(f"❌ {name} - FAILED: {e}")
            all_good = False
    
    return all_good

def main():
    """Main installation function"""
    print("🚀 Negotiator Bot - Python 3.13 Compatible Installation")
    print("=" * 60)
    
    # Check Python version
    is_py313 = check_python_version()
    
    # Install system dependencies
    install_system_dependencies()
    
    # Install Python packages
    install_python_packages()
    
    # Verify installation
    if verify_installation():
        print("\n🎉 Installation completed successfully!")
        print("\n🚀 You can now run the application:")
        print("   Streamlit: streamlit run streamlit_app.py")
        print("   Flask: python main.py")
    else:
        print("\n❌ Installation completed with errors.")
        print("Please check the error messages above and try installing missing packages manually.")
    
    print("\n📚 For more help, see DEPLOYMENT_PY313.md")

if __name__ == "__main__":
    main()
