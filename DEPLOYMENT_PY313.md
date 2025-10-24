# 🚀 Python 3.13 Deployment Guide

## ⚠️ Python 3.13 Compatibility Issues

Python 3.13 has compatibility issues with older versions of some packages. This guide provides solutions for deploying the Negotiator Bot with Python 3.13.

## 🔧 Fixed Requirements

### Updated Package Versions

- **Pillow**: Updated from 10.0.1 to 12.0.0 (Python 3.13 compatible)
- **reportlab**: Updated from 4.0.4 to 4.4.4 (Python 3.13 compatible)
- **All other packages**: Kept at stable versions

### Installation Commands

#### For Streamlit Version (Recommended)

```bash
pip install -r requirements_py313.txt
```

#### For Flask Version

```bash
pip install -r requirements.txt
```

## 🐛 Common Python 3.13 Issues & Solutions

### 1. Pillow Build Error

**Error**: `KeyError: '__version__'` during Pillow installation

**Solution**: Use Pillow 12.0.0 or later

```bash
pip install Pillow>=12.0.0
```

### 2. reportlab Build Error

**Error**: Build backend failed to determine requirements

**Solution**: Use reportlab 4.4.4 or later

```bash
pip install reportlab>=4.4.4
```

### 3. setuptools Issues

**Error**: setuptools build_meta errors

**Solution**: Update setuptools

```bash
pip install --upgrade setuptools wheel
```

## 🚀 Deployment Steps

### Step 1: Environment Setup

```bash
# Create virtual environment
python3.13 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel
```

### Step 2: Install Dependencies

```bash
# For Streamlit version
pip install -r requirements_py313.txt

# Or for Flask version
pip install -r requirements.txt
```

### Step 3: Run Application

#### Streamlit Version

```bash
streamlit run streamlit_app.py --server.port 8501
```

#### Flask Version

```bash
python main.py
```

## 🔍 Troubleshooting

### If you still get Pillow errors:

```bash
# Try installing Pillow with specific build requirements
pip install --upgrade pip setuptools wheel
pip install --no-cache-dir Pillow==12.0.0
```

### If you get reportlab errors:

```bash
# Install reportlab with specific version
pip install --no-cache-dir reportlab==4.4.4
```

### If you get setuptools errors:

```bash
# Force reinstall setuptools
pip install --force-reinstall setuptools
```

## 📦 Alternative Installation Methods

### Using uv (if available)

```bash
uv pip install -r requirements_py313.txt
```

### Using conda

```bash
conda create -n negotiator-bot python=3.13
conda activate negotiator-bot
pip install -r requirements_py313.txt
```

### Using poetry

```toml
[tool.poetry.dependencies]
python = "^3.13"
streamlit = "^1.28.0"
openai = "^1.0.0"
python-dotenv = "^1.0.0"
Pillow = "^12.0.0"
reportlab = "^4.4.4"
Flask = "^2.3.3"
gunicorn = "^21.2.0"
httpx = "^0.24.1"
```

## 🎯 Platform-Specific Notes

### Ubuntu/Debian

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3.13-dev python3.13-venv
sudo apt-get install libjpeg-dev zlib1g-dev

# Then install Python packages
pip install -r requirements_py313.txt
```

### macOS

```bash
# Install Xcode command line tools
xcode-select --install

# Install Python packages
pip install -r requirements_py313.txt
```

### Windows

```bash
# Install Visual Studio Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Install Python packages
pip install -r requirements_py313.txt
```

## ✅ Verification

After installation, verify everything works:

```bash
# Test Streamlit
python -c "import streamlit; print('Streamlit OK')"

# Test OpenAI
python -c "import openai; print('OpenAI OK')"

# Test Pillow
python -c "from PIL import Image; print('Pillow OK')"

# Test reportlab
python -c "from reportlab.pdfgen import canvas; print('reportlab OK')"
```

## 🚀 Production Deployment

### Using Gunicorn (Flask version)

```bash
gunicorn -w 4 -b 0.0.0.0:8080 main:app
```

### Using Streamlit (Streamlit version)

```bash
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

### Using Docker

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements_py313.txt .
RUN pip install --no-cache-dir -r requirements_py313.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Run application
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

## 📞 Support

If you encounter issues with Python 3.13:

1. **Check Python version**: `python --version`
2. **Update pip**: `pip install --upgrade pip`
3. **Update setuptools**: `pip install --upgrade setuptools wheel`
4. **Use compatible versions**: Use `requirements_py313.txt`
5. **Check system dependencies**: Ensure build tools are installed

---

**Happy Deploying! 🚀**
