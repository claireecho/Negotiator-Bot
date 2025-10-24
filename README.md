# 🤖 Recruiter Bot

A smart AI-powered recruiter bot that presents job offers and negotiates with candidates using OpenAI's GPT API. The bot evaluates negotiation attempts and can improve offers for deserving candidates or decline unreasonable requests.

## ✨ Features

- **Smart Negotiation**: Uses GPT-3.5-turbo to evaluate candidate negotiations
- **Dynamic Offers**: Three-tier offer system (Entry, Mid, Senior level positions)
- **Real-time Chat**: Interactive web interface for seamless conversation
- **Professional UI**: Modern, responsive design with smooth animations
- **Offer Management**: Visual display of current offers with benefits and salary ranges
- **Intelligent Responses**: Bot can improve, maintain, or decline offers based on negotiation quality

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd recruiter-bot
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Create a `.env` file in the project root:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   Or set the environment variable directly:

   ```bash
   export OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**

   ```bash
   python main.py
   ```

5. **Access the application**

   - Open your browser and go to `http://localhost:5000`
   - The app will be running locally on your machine

## 🌐 Deployment Options

### Local Development

The app runs locally on `http://localhost:5000` by default.

### Cloud Deployment

You can deploy this application to various cloud platforms:

- **Heroku**: Add a `Procfile` with `web: gunicorn main:app`
- **Railway**: Connect your GitHub repository
- **DigitalOcean App Platform**: Deploy directly from GitHub
- **AWS/GCP/Azure**: Use their respective container services
- **Docker**: Create a Dockerfile for containerized deployment

### Environment Variables for Production

Make sure to set these environment variables in your deployment platform:

- `OPENAI_API_KEY`: Your OpenAI API key
- `PORT`: Port number (usually set automatically by the platform)

## 🎯 How It Works

### Initial Offer Generation

- The bot randomly selects from three job offer levels:
  - **Entry Level**: Junior Software Developer ($45,000-$55,000)
  - **Mid Level**: Software Developer ($65,000-$80,000)
  - **Senior Level**: Senior Software Developer ($85,000-$110,000)

### Negotiation Process

1. **User starts conversation** → Bot presents initial offer
2. **User negotiates** → Bot evaluates using GPT API
3. **Bot responds** with one of three actions:
   - **Improve**: Upgrade to higher level or add benefits
   - **Maintain**: Keep current offer
   - **Decline**: End negotiation (for unreasonable requests)

### GPT Evaluation Criteria

The bot considers:

- Candidate's negotiation skills
- Reasonableness of requests
- Professional communication
- Market value of requested improvements

## 🛠️ Technical Details

### Architecture

- **Backend**: Flask web framework
- **AI**: OpenAI GPT-3.5-turbo API
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Deployment**: Any Python hosting platform (Heroku, Railway, DigitalOcean, etc.)

### Key Files

- `main.py` - Main Flask application with bot logic
- `templates/index.html` - Web interface
- `static/css/style.css` - Styling and responsive design
- `requirements.txt` - Python dependencies

### API Endpoints

- `GET /` - Main application page
- `POST /start_conversation` - Initialize bot conversation
- `POST /negotiate` - Handle user negotiation attempts
- `GET /health` - Health check endpoint

## 🎨 Customization

### Adding New Offer Levels

Edit the `JOB_OFFERS` dictionary in `main.py`:

```python
JOB_OFFERS = {
    "your_level": {
        "title": "Your Job Title",
        "salary": "$X,XXX - $Y,YYY",
        "benefits": ["Benefit 1", "Benefit 2"],
        "description": "Job description"
    }
}
```

### Modifying Bot Personality

Update the `system_prompt` in the `evaluate_negotiation` function to change:

- Bot's communication style
- Evaluation criteria
- Response format

### Styling Changes

Modify `static/css/style.css` to customize:

- Colors and gradients
- Layout and spacing
- Animations and transitions
- Responsive breakpoints

## 🔧 Environment Variables

| Variable         | Description                        | Required |
| ---------------- | ---------------------------------- | -------- |
| `OPENAI_API_KEY` | Your OpenAI API key                | Yes      |
| `PORT`           | Port for Flask app (default: 5000) | No       |

## 📱 Usage Tips

### For Candidates

- Be professional and respectful in negotiations
- Highlight relevant skills and experience
- Make reasonable requests based on market rates
- Show enthusiasm for the role

### For Recruiters

- Monitor conversation logs for insights
- Adjust offer levels based on company needs
- Customize evaluation criteria for different roles

## 🚨 Troubleshooting

### Common Issues

1. **"OpenAI API key not found"**

   - Ensure `OPENAI_API_KEY` is set as an environment variable
   - Check for typos in the environment variable name

2. **"Error processing your message"**

   - Check your OpenAI API quota and billing
   - Verify internet connection
   - Check application logs for detailed error messages

3. **Styling not loading**
   - Ensure `static/css/style.css` exists
   - Check Flask static file configuration
   - Clear browser cache

### Debug Mode

The app runs in debug mode by default. To disable:

```python
app.run(host='0.0.0.0', port=port, debug=False)
```

## 🔒 Security Considerations

- Never commit API keys to version control
- Use environment variables for sensitive data
- Consider rate limiting for production use
- Validate user inputs to prevent injection attacks

## 📈 Future Enhancements

- [ ] User authentication and session management
- [ ] Conversation history persistence
- [ ] Multiple job categories and industries
- [ ] Advanced analytics and reporting
- [ ] Integration with HR systems
- [ ] Multi-language support

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the application logs for error messages
3. Ensure all dependencies are properly installed
4. Verify your OpenAI API key is valid and has sufficient credits

---

**Happy negotiating! 🎉**
