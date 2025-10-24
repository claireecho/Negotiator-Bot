# 🤖 Recruiter Bot

A smart AI-powered recruiter bot that presents job offers and negotiates with candidates using OpenAI's GPT API. The bot evaluates negotiation attempts and can improve offers for deserving candidates or decline unreasonable requests.

## ✨ Features

- **AI-Powered Negotiation**: Uses GPT-3.5-turbo to evaluate candidate negotiations with realistic recruiter behavior
- **Real Company Offers**: Personalized offers from actual tech companies (Google, Microsoft, Apple, Amazon, Airbnb, Stripe, etc.)
- **Professional PDF Generation**: Download detailed offer letters as PDFs that match your exact offer
- **Progressive Difficulty**: Negotiations become more challenging with each attempt - first try is moderate, subsequent attempts are much stricter
- **Company Preservation**: Offers maintain the same company and position throughout negotiations - only compensation improves
- **Change Explanations**: Clear explanations of what specifically changed in improved offers
- **Four-Tier System**: New Grad, Entry, Mid, and Senior level positions with appropriate compensation and benefits
- **Real-time Chat**: Interactive web interface for seamless conversation
- **Professional UI**: Modern, responsive design with smooth animations and collapsible offer display
- **Offer Management**: Visual display of current offers with company branding, benefits, equity, and signing bonuses
- **Intelligent Responses**: Bot can improve, maintain, decline, or withdraw offers based on negotiation quality and attempt number
- **Offer Withdrawal**: Bot can withdraw offers for unprofessional, demanding, or disrespectful behavior
- **User-Friendly Setup**: No environment variables needed - enter your OpenAI API key directly in the web interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (get one from [OpenAI](https://platform.openai.com/api-keys))

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

3. **Run the application**

   ```bash
   python main.py
   ```

4. **Access the application**

   - Open your browser and go to `http://localhost:8080`
   - The app will be running locally on your machine

5. **Enter your OpenAI API key**

   - When you first visit the app, you'll see a field to enter your OpenAI API key
   - Enter your API key (starts with `sk-`) and click "Save API Key"
   - Your API key is stored locally in your browser and never sent to our servers
   - Once saved, you can start negotiating with the recruiter bot!

## 🌐 Deployment Options

### Local Development

The app runs locally on `http://localhost:8080` by default.

### Cloud Deployment

You can deploy this application to various cloud platforms:

- **Heroku**: Add a `Procfile` with `web: gunicorn main:app`
- **Railway**: Connect your GitHub repository
- **DigitalOcean App Platform**: Deploy directly from GitHub
- **AWS/GCP/Azure**: Use their respective container services
- **Docker**: Create a Dockerfile for containerized deployment

### Environment Variables for Production

Make sure to set these environment variables in your deployment platform:

- `PORT`: Port number (usually set automatically by the platform)

**Note**: Users will enter their OpenAI API keys directly in the web interface, so no server-side API key configuration is needed.

## 🎯 How It Works

### Initial Offer Generation

- The bot randomly selects from four official job offer levels:
  - **New Grad**: New Grad Software Engineer ($75,000)
  - **Entry Level**: Software Engineer I ($85,000)
  - **Mid Level**: Software Engineer II ($105,000)
  - **Senior Level**: Senior Software Engineer ($130,000)

### Negotiation Process

1. **User starts conversation** → Bot presents a firm, realistic job offer
2. **User negotiates** → Bot evaluates using GPT API with strict criteria
3. **Bot responds** with one of three actions:
   - **Improve**: Upgrade to higher level or add benefits (only for compelling arguments)
   - **Maintain**: Keep current offer (most common outcome)
   - **Decline**: End negotiation (for unreasonable/unprofessional requests)

### GPT Evaluation Criteria

The bot acts like a real recruiter and only improves offers when candidates demonstrate:

- **Exceptional Skills**: Experience beyond role requirements
- **Strong Negotiation**: Logical reasoning and professional communication
- **Specific Value**: Clear benefits they bring to the company
- **Market Research**: Knowledge of industry rates and standards

**Examples of Good Negotiations:**

- "I have 8 years of React experience and led a team of 5 developers. I also have AWS certifications valuable for this role."
- "Market research shows senior developers with my microservices expertise typically earn $130,000-$150,000. I bring expertise that could save the company significant development time."

**Examples of Bad Negotiations:**

- "I need more money"
- "This offer is too low"
- "Can you increase the salary?"

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

| Variable | Description                        | Required |
| -------- | ---------------------------------- | -------- |
| `PORT`   | Port for Flask app (default: 8080) | No       |

**Note**: The OpenAI API key is now entered directly in the web interface, so no environment variables are needed for the API key.

## 📱 Usage Tips

### For Candidates

- **Be Professional**: Maintain respectful, business-like communication
- **Provide Evidence**: Back up requests with specific skills, experience, or market data
- **Research Market Rates**: Know industry standards for your role and experience level
- **Highlight Value**: Explain how your skills benefit the company specifically
- **Be Specific**: Instead of "I want more money," say "Based on my 5 years of React experience and team leadership, I believe I qualify for the senior level"
- **Show Enthusiasm**: Express genuine interest in the role and company
- **Be Reasonable**: Understand that most negotiations result in maintaining the current offer

### For Recruiters

- Monitor conversation logs for insights
- Adjust offer levels based on company needs
- Customize evaluation criteria for different roles

## 🚨 Troubleshooting

### Common Issues

1. **"API key is required" or "Invalid API key format"**

   - Make sure you've entered your OpenAI API key in the web interface
   - Ensure your API key starts with `sk-` and is at least 20 characters long
   - Get a valid API key from [OpenAI Platform](https://platform.openai.com/api-keys)

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

## 🎯 How to Use

1. **Start the application** and open your browser to `http://localhost:8080`
2. **Enter your OpenAI API key** in the provided field
3. **Click "Start Conversation"** to begin with an initial job offer from a real company
4. **Review the offer** displayed in the collapsible offer section (click header to expand/collapse)
5. **Type your negotiation message** in the input field - be specific and professional
6. **Send your message** and see the recruiter's response
7. **If offer improves**, you'll see exactly what changed with clear explanations
8. **Continue negotiating** - but remember, each attempt becomes more difficult
9. **Download PDF** of your current offer anytime using the download button
10. **Change API key** anytime using the change button

## 💡 Negotiation Tips

### ✅ Good Negotiation Examples:

- "I have 5 years of experience in React and led a team of 3 developers at my previous company, plus I have AWS certifications"
- "I have competing offers from Google for $120k and Microsoft for $115k respectively"
- "I bring specialized skills in machine learning that directly match your AI initiatives"

### ❌ Poor Negotiation Examples:

- "I want more money"
- "I think I deserve better"
- "Can you increase the salary?"
- "I'm really good at coding"

### 🚫 Withdrawal-Worthy Examples (will result in offer withdrawal):

- "This is insulting, I deserve way more than this"
- "You're being cheap, I know you can afford more"
- "This is pathetic, I expected better from [company name]"
- "I'm not accepting anything less than $200k"
- "You're making a mistake if you don't give me what I want"
- "I have other offers, you better match them or I'm gone"

### 🎯 Strategy:

- **First attempt**: Be specific about your value and experience
- **Second attempt**: Provide concrete evidence of competing offers or unique skills
- **Third+ attempts**: Only try if you have exceptional qualifications - the bot becomes very strict

## 🏢 Supported Companies

The bot can present offers from these real tech companies:

**Tech Giants:**

- Google 🔍
- Microsoft 🪟
- Apple 🍎
- Amazon 📦

**Startups:**

- Stripe 💳
- Airbnb 🏠
- Slack 💬

**Fintech:**

- PayPal 💰
- Square ⬜

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
