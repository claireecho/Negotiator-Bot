import os
import json
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import random

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
# Sample job offers with different levels
JOB_OFFERS = {
    "entry": {
        "title": "Junior Software Developer",
        "salary": "$45,000 - $55,000",
        "benefits": ["Health Insurance", "401k", "15 days PTO"],
        "description": "Entry-level position for recent graduates"
    },
    "mid": {
        "title": "Software Developer",
        "salary": "$65,000 - $80,000", 
        "benefits": ["Health Insurance", "401k", "20 days PTO", "Stock Options"],
        "description": "Mid-level position for experienced developers"
    },
    "senior": {
        "title": "Senior Software Developer",
        "salary": "$85,000 - $110,000",
        "benefits": ["Health Insurance", "401k", "25 days PTO", "Stock Options", "Flexible Hours"],
        "description": "Senior position for experienced professionals"
    }
}

def generate_initial_offer():
    """Generate an initial job offer based on user profile"""
    offer_level = random.choice(["entry", "mid", "senior"])
    return JOB_OFFERS[offer_level], offer_level

def evaluate_negotiation(user_message, current_offer, offer_level, conversation_history):
    """Use GPT to evaluate negotiation and determine response"""
    
    system_prompt = f"""You are a professional recruiter for a tech company. You have made an initial offer for a {JOB_OFFERS[offer_level]['title']} position.

Current Offer Details:
- Position: {JOB_OFFERS[offer_level]['title']}
- Salary: {JOB_OFFERS[offer_level]['salary']}
- Benefits: {', '.join(JOB_OFFERS[offer_level]['benefits'])}
- Description: {JOB_OFFERS[offer_level]['description']}

Your job is to:
1. Listen to the candidate's negotiation attempts
2. Evaluate if they deserve a better offer based on their skills, experience, and negotiation approach
3. If they're worth it, improve the offer (move to next level or add benefits)
4. If they're not worth it or being unreasonable, politely decline or maintain current offer
5. Always maintain a professional, friendly tone

Available offer levels:
- Entry: $45,000-$55,000 (basic benefits)
- Mid: $65,000-$80,000 (better benefits + stock)
- Senior: $85,000-$110,000 (best benefits + flexibility)

Respond in JSON format with:
{{
    "response": "Your response to the candidate",
    "action": "improve" | "maintain" | "decline",
    "new_offer_level": "entry" | "mid" | "senior" | null,
    "reasoning": "Brief explanation of your decision"
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Candidate says: {user_message}"}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        response_text = response.choices[0].message.content
        return json.loads(response_text)
        
    except Exception as e:
        return {
            "response": "I apologize, but I'm having trouble processing your request right now. Could you please try again?",
            "action": "maintain",
            "new_offer_level": None,
            "reasoning": "Technical error occurred"
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_conversation', methods=['POST'])
def start_conversation():
    """Start a new conversation with an initial offer"""
    initial_offer, offer_level = generate_initial_offer()
    
    return jsonify({
        'offer': initial_offer,
        'offer_level': offer_level,
        'message': f"Hello! I'm excited to present you with an opportunity. We'd like to offer you a position as a {initial_offer['title']} with a salary range of {initial_offer['salary']}. The role includes {', '.join(initial_offer['benefits'])}. What do you think about this offer?"
    })

@app.route('/negotiate', methods=['POST'])
def negotiate():
    """Handle negotiation attempts"""
    data = request.json
    user_message = data.get('message', '')
    current_offer_level = data.get('offer_level', 'entry')
    conversation_history = data.get('history', [])
    
    if not user_message.strip():
        return jsonify({'error': 'Please provide a message'}), 400
    
    # Evaluate the negotiation
    evaluation = evaluate_negotiation(user_message, JOB_OFFERS[current_offer_level], current_offer_level, conversation_history)
    
    response_data = {
        'response': evaluation['response'],
        'action': evaluation['action'],
        'reasoning': evaluation['reasoning']
    }
    
    # Update offer if improved
    if evaluation['action'] == 'improve' and evaluation['new_offer_level']:
        new_level = evaluation['new_offer_level']
        response_data['new_offer'] = JOB_OFFERS[new_level]
        response_data['new_offer_level'] = new_level
    elif evaluation['action'] == 'maintain':
        response_data['current_offer'] = JOB_OFFERS[current_offer_level]
        response_data['offer_level'] = current_offer_level
    elif evaluation['action'] == 'decline':
        response_data['offer_declined'] = True
    
    return jsonify(response_data)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
