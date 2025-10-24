# 🤖 Negotiator Bot vs Recruiter Bot - Streamlit Version

A real-time negotiation simulation between an AI-powered Negotiator Bot and a Recruiter Bot, built with Streamlit.

## 🚀 Quick Start

### Option 1: Using the launcher script

```bash
python run_streamlit.py
```

### Option 2: Direct Streamlit command

```bash
streamlit run streamlit_app.py
```

### Option 3: With custom port

```bash
streamlit run streamlit_app.py --server.port 8501
```

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key

## 🛠️ Installation

1. **Install dependencies:**

   ```bash
   pip install -r requirements_streamlit.txt
   ```

2. **Run the application:**

   ```bash
   streamlit run streamlit_app.py
   ```

3. **Open your browser:**
   - The app will automatically open at `http://localhost:8501`
   - If not, manually navigate to the URL shown in the terminal

## 🎯 Features

### 🤖 AI-Powered Negotiation

- **Negotiator Bot**: Uses advanced negotiation strategies and psychological tactics
- **Recruiter Bot**: Responds dynamically to negotiation attempts
- **Real-time Communication**: Watch bots negotiate in real-time

### 📊 Live Statistics

- **Current Salary**: Real-time salary tracking
- **Negotiation Rounds**: Count of negotiation attempts
- **Salary Increase**: Total increase achieved
- **Percentage Increase**: Percentage improvement

### 🎨 Interactive Interface

- **Modern UI**: Clean, responsive design
- **Real-time Chat**: Live conversation display
- **Typing Indicators**: Visual feedback during bot "thinking"
- **Sidebar Controls**: Easy start/stop and statistics

## 🎮 How to Use

1. **Enter API Key**: Input your OpenAI API key in the sidebar
2. **Start Negotiation**: Click "🚀 Start Negotiation" to begin
3. **Watch the Bots**: Observe the AI-powered negotiation unfold
4. **Monitor Progress**: Track salary increases and negotiation rounds
5. **Stop Anytime**: Click "⏹️ Stop" to end the simulation

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Customization

- **Salary Progression**: Modify `RecruiterBot.salary_progression`
- **Response Templates**: Update `RecruiterBot.responses`
- **Negotiation Strategies**: Customize in `main.py`

## 📈 Expected Results

The negotiation typically results in:

- **Initial Salary**: $85,000
- **Final Salary**: $95,000 - $100,000
- **Total Increase**: $10,000 - $15,000
- **Success Rate**: 80-90% of negotiations result in salary increases

## 🎯 Negotiation Strategies

### Negotiator Bot Tactics

- **Market Research**: References industry standards and market data
- **Competing Offers**: Creates urgency with alternative opportunities
- **Value Proposition**: Emphasizes ROI and quantified achievements
- **Psychological Pressure**: Uses scarcity and FOMO techniques
- **Creative Solutions**: Suggests performance bonuses and equity

### Recruiter Bot Responses

- **Progressive Increases**: Gradually increases offers based on negotiation quality
- **Flexible Approach**: Shows willingness to negotiate
- **Value Recognition**: Acknowledges candidate's worth
- **Competitive Positioning**: Responds to market pressure

## 🚀 Deployment

### Local Development

```bash
streamlit run streamlit_app.py --server.port 8501
```

### Production Deployment

```bash
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

### Docker (Optional)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements_streamlit.txt .
RUN pip install -r requirements_streamlit.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**

   - Ensure your OpenAI API key is valid
   - Check that you have sufficient credits

2. **Import Errors**

   - Install all requirements: `pip install -r requirements_streamlit.txt`
   - Ensure `main.py` is in the same directory

3. **Port Already in Use**

   - Use a different port: `streamlit run streamlit_app.py --server.port 8502`

4. **Slow Responses**
   - Check your internet connection
   - OpenAI API may be experiencing delays

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

**Happy Negotiating! 🤖💼**
