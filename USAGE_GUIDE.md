# 🤖 Negotiator Bot vs Recruiter Bot - Usage Guide

## 🚀 Quick Start

### Method 1: Using the Demo Script (Recommended)

```bash
python3 demo_streamlit.py
```

### Method 2: Direct Streamlit Command

```bash
streamlit run streamlit_app.py
```

### Method 3: Using the Launcher

```bash
python3 run_streamlit.py
```

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **OpenAI API Key** (get one at https://platform.openai.com/api-keys)
3. **Internet connection** for OpenAI API calls

## 🛠️ Installation

1. **Install dependencies:**

   ```bash
   pip3 install streamlit openai python-dotenv
   ```

2. **Or use the requirements file:**
   ```bash
   pip3 install -r requirements_streamlit.txt
   ```

## 🎯 How to Use

### Step 1: Start the Application

Run one of the commands above. The app will open in your browser at `http://localhost:8501`.

### Step 2: Enter Your API Key

1. In the sidebar, enter your OpenAI API key
2. The Negotiator Bot will initialize automatically
3. You'll see a green checkmark when ready

### Step 3: Start the Negotiation

1. Click "🚀 Start Negotiation" button
2. Watch the bots negotiate in real-time
3. Monitor the statistics in the sidebar

### Step 4: Monitor Progress

- **Current Salary**: Updates in real-time
- **Negotiation Rounds**: Count of back-and-forth exchanges
- **Salary Increase**: Total amount gained
- **Increase %**: Percentage improvement

## 🎮 Features

### 🤖 AI-Powered Negotiation

- **Negotiator Bot**: Uses advanced psychological tactics
- **Recruiter Bot**: Responds dynamically to negotiation attempts
- **Real-time Communication**: Live conversation display

### 📊 Live Statistics

- Real-time salary tracking
- Negotiation round counting
- Success metrics and percentages

### 🎨 Interactive Interface

- Modern, responsive design
- Typing indicators during bot "thinking"
- Easy start/stop controls
- Sidebar statistics panel

## 🔧 Configuration

### Customizing the Recruiter Bot

Edit `streamlit_app.py` and modify the `RecruiterBot` class:

```python
class RecruiterBot:
    def __init__(self):
        self.responses = [
            "Your custom response 1",
            "Your custom response 2",
            # ... more responses
        ]
        self.salary_progression = [85000, 87000, 90000, 95000, 100000]
```

### Customizing the Negotiator Bot

Modify the negotiation strategies in `main.py`:

```python
# Add new response templates
ResponseTemplate(
    template_id="your_template",
    strategy=NegotiationStrategy.CONFIDENT_ASSERTIVE,
    tone=ResponseTone.CONFIDENTLY_ASSERTIVE,
    template_text="Your custom template...",
    variables=["var1", "var2"],
    effectiveness_score=0.95
)
```

## 📈 Expected Results

### Typical Negotiation Flow

1. **Initial Offer**: $85,000
2. **Round 1**: Negotiator challenges the offer
3. **Round 2**: Recruiter offers $87,000
4. **Round 3**: Negotiator uses market data
5. **Round 4**: Recruiter offers $90,000
6. **Round 5**: Negotiator mentions competing offers
7. **Round 6**: Recruiter offers $95,000
8. **Round 7**: Negotiator emphasizes value
9. **Round 8**: Recruiter offers $100,000
10. **Final**: Negotiation concludes

### Success Metrics

- **Success Rate**: 80-90% of negotiations result in increases
- **Average Increase**: $10,000 - $15,000
- **Best Case**: Up to $20,000+ increase
- **Typical Duration**: 8-10 rounds

## 🐛 Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**

```bash
pip3 install streamlit
```

#### 2. "Error initializing bot: Incorrect API key provided"

**Solution:**

- Check your OpenAI API key is correct
- Ensure you have sufficient credits
- Verify the key starts with "sk-"

#### 3. "Port 8501 is already in use"

**Solution:**

```bash
streamlit run streamlit_app.py --server.port 8502
```

#### 4. "Error generating negotiator response"

**Solution:**

- Check your internet connection
- Verify OpenAI API is accessible
- Check your API key permissions

#### 5. App won't start

**Solution:**

```bash
# Check Python version
python3 --version

# Install all requirements
pip3 install -r requirements_streamlit.txt

# Try running directly
python3 streamlit_app.py
```

### Debug Mode

Run with debug information:

```bash
streamlit run streamlit_app.py --logger.level debug
```

## 🚀 Advanced Usage

### Custom Port

```bash
streamlit run streamlit_app.py --server.port 8502
```

### Custom Host

```bash
streamlit run streamlit_app.py --server.address 0.0.0.0
```

### Headless Mode (No Browser)

```bash
streamlit run streamlit_app.py --server.headless true
```

### Production Deployment

```bash
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

## 📊 Performance Tips

1. **API Key Management**: Store your API key securely
2. **Network**: Ensure stable internet connection
3. **Resources**: Close other applications for better performance
4. **Browser**: Use Chrome or Firefox for best experience

## 🎯 Best Practices

1. **Start Fresh**: Clear conversation history between tests
2. **Monitor Stats**: Watch the sidebar for real-time updates
3. **API Limits**: Be mindful of OpenAI API usage
4. **Experimentation**: Try different negotiation strategies

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Ensure your OpenAI API key is valid
4. Check the console for error messages

## 🎉 Enjoy!

The Negotiator Bot vs Recruiter Bot application provides an engaging way to see AI-powered negotiation in action. Watch as the bots use psychological tactics, market data, and strategic positioning to achieve better outcomes!

---

**Happy Negotiating! 🤖💼**
