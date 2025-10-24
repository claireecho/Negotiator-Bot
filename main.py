import os
import json
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
    
# Sample job offers with different levels
JOB_OFFERS = {
    "newgrad": {
        "title": "New Grad Software Engineer",
        "salary": "$75,000",
        "benefits": ["Health Insurance", "401k with 4% match", "15 days PTO", "Learning & Development Budget"],
        "description": "Entry-level position for recent computer science graduates with 0-1 years experience"
    },
    "entry": {
        "title": "Software Engineer I",
        "salary": "$85,000",
        "benefits": ["Health Insurance", "401k with 4% match", "18 days PTO", "Stock Options"],
        "description": "Junior position for developers with 1-3 years of experience"
    },
    "mid": {
        "title": "Software Engineer II",
        "salary": "$105,000", 
        "benefits": ["Health Insurance", "401k with 6% match", "20 days PTO", "Stock Options", "Annual Bonus"],
        "description": "Mid-level position for experienced developers with 3-6 years experience"
    },
    "senior": {
        "title": "Senior Software Engineer",
        "salary": "$130,000",
        "benefits": ["Health Insurance", "401k with 6% match", "25 days PTO", "Stock Options", "Annual Bonus", "Flexible Hours"],
        "description": "Senior position for experienced professionals with 6+ years experience"
    }
}

def generate_initial_offer():
    """Generate an initial job offer based on user profile"""
    offer_level = random.choice(["newgrad", "entry", "mid", "senior"])
    return JOB_OFFERS[offer_level], offer_level

def evaluate_negotiation(user_message, current_offer, offer_level, conversation_history, api_key):
    """Use GPT to evaluate negotiation and determine response"""
    
    system_prompt = f"""You are a professional recruiter for a tech company. You have made a firm initial offer for a {JOB_OFFERS[offer_level]['title']} position.

CURRENT OFFER DETAILS:
- Position: {JOB_OFFERS[offer_level]['title']}
- Salary: {JOB_OFFERS[offer_level]['salary']}
- Benefits: {', '.join(JOB_OFFERS[offer_level]['benefits'])}
- Description: {JOB_OFFERS[offer_level]['description']}

IMPORTANT: This is a REAL job offer. The candidate must negotiate professionally and persuasively to get improvements. You are NOT generous - you only improve offers for truly compelling arguments.

NEGOTIATION RULES:
1. The initial offer is fair and competitive for the market
2. You only improve offers when candidates demonstrate:
   - Exceptional skills or experience beyond the role requirements
   - Strong negotiation skills with logical reasoning
   - Specific value they bring to the company
   - Professional communication and respect
3. Generic requests like "I want more money" are rejected
4. Unreasonable demands or unprofessional behavior result in offer withdrawal
5. You maintain a professional but firm tone

AVAILABLE OFFER LEVELS:
- New Grad: $75,000 (basic benefits + learning budget) - for recent CS graduates
- Entry: $85,000 (basic benefits + stock) - for developers with 1-3 years experience
- Mid: $105,000 (better benefits + stock + bonus) - for experienced developers
- Senior: $130,000 (best benefits + stock + bonus + flexibility) - for senior professionals

RESPONSE FORMAT (JSON):
{{
    "response": "Your professional response to the candidate",
    "action": "improve" | "maintain" | "decline",
    "new_offer_level": "newgrad" | "entry" | "mid" | "senior" | null,
    "reasoning": "Brief explanation of your decision"
}}

EXAMPLES OF GOOD NEGOTIATIONS:
- "I have 8 years of experience in React and led a team of 5 developers at my previous company. I also have AWS certifications that would be valuable for this role."
- "I've reviewed the market rates for this position and my research shows senior developers with my skill set typically earn $90,000-$100,000. I bring expertise in microservices architecture that could save the company significant development time."

EXAMPLES OF BAD NEGOTIATIONS:
- "I need more money"
- "This offer is too low"
- "Can you increase the salary?"
- "I want better benefits"

Be realistic and professional. Most negotiations should result in "maintain" unless the candidate provides compelling evidence of their value."""

    try:
        # Create a new client instance with the user's API key
        user_client = OpenAI(api_key=api_key)
        
        response = user_client.chat.completions.create(
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
        print(f"Error in evaluate_negotiation: {e}")
        print(f"Error type: {type(e)}")
        print(f"API key provided: {api_key[:10]}..." if api_key else "No API key")
        return {
            "response": f"I apologize, but I'm having trouble processing your request right now. Error: {str(e)}",
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
    data = request.json
    api_key = data.get('api_key')
    
    if not api_key:
        return jsonify({'error': 'API key is required'}), 400
    
    # Validate API key format
    if not api_key.startswith('sk-') or len(api_key) < 20:
        return jsonify({'error': 'Invalid API key format'}), 400
    
    initial_offer, offer_level = generate_initial_offer()
    
    return jsonify({
        'offer': initial_offer,
        'offer_level': offer_level,
        'message': f"Thank you for your interest in joining our team. After reviewing your application, we're pleased to extend you an offer for the {initial_offer['title']} position. The salary is {initial_offer['salary']} with comprehensive benefits including {', '.join(initial_offer['benefits'])}. This offer reflects our assessment of your qualifications and the market rate for this role. Do you have any questions about the offer?"
    })

@app.route('/negotiate', methods=['POST'])
def negotiate():
    """Handle negotiation attempts"""
    data = request.json
    user_message = data.get('message', '')
    current_offer_level = data.get('offer_level', 'entry')
    conversation_history = data.get('history', [])
    api_key = data.get('api_key')
    
    print(f"Negotiate request received:")
    print(f"  Message: {user_message}")
    print(f"  Offer level: {current_offer_level}")
    print(f"  API key: {api_key[:10]}..." if api_key else "  API key: None")
    
    if not user_message.strip():
        return jsonify({'error': 'Please provide a message'}), 400
    
    if not api_key:
        return jsonify({'error': 'API key is required'}), 400
    
    # Validate API key format
    if not api_key.startswith('sk-') or len(api_key) < 20:
        return jsonify({'error': 'Invalid API key format'}), 400
    
    # Evaluate the negotiation
    evaluation = evaluate_negotiation(user_message, JOB_OFFERS[current_offer_level], current_offer_level, conversation_history, api_key)
    
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

    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
