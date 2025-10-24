import streamlit as st
import time
import json
from datetime import datetime
from main import NegotiatorBot, NegotiationStrategy, ResponseTone, NegotiationContext, ResponseTemplate
from dataclasses import dataclass
from typing import List, Dict
import random

# Page configuration
st.set_page_config(
    page_title="Negotiator Bot vs Recruiter Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .bot-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 4px solid;
    }
    
    .negotiator-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    
    .recruiter-message {
        background-color: #f3e5f5;
        border-left-color: #9c27b0;
    }
    
    .system-message {
        background-color: #fff3e0;
        border-left-color: #ff9800;
    }
    
    .typing-indicator {
        font-style: italic;
        color: #666;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.3; }
    }
    
    .stats-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'negotiator_bot' not in st.session_state:
    st.session_state.negotiator_bot = None
if 'context_id' not in st.session_state:
    st.session_state.context_id = None
if 'current_salary' not in st.session_state:
    st.session_state.current_salary = 85000
if 'round_count' not in st.session_state:
    st.session_state.round_count = 0
if 'conversation_active' not in st.session_state:
    st.session_state.conversation_active = False

# Recruiter Bot Class
class RecruiterBot:
    def __init__(self):
        self.responses = [
            "Thank you for your interest in joining our team! After reviewing your application, we're pleased to extend you an offer for the Software Engineer II position. The salary is $85,000 with comprehensive benefits including health insurance, 401k with 4% match, and 18 days PTO. This offer reflects our assessment of your qualifications and the market rate for this role. Do you have any questions about the offer?",
            "We understand your perspective. You make some good points. Let me see what I can do - I can bump this to $87,000.",
            "I appreciate your research and market knowledge. Let me talk to my manager about improving this offer.",
            "You're clearly talented and we don't want to lose you. I've spoken with compensation and we can go up to $90,000.",
            "I understand your concerns about market rates. Given your strong negotiation and the value you bring, we're willing to increase our offer.",
            "We're excited about your potential and don't want this opportunity to slip away. Let's talk about what it would take to get you to yes.",
            "Thank you for your patience. After reviewing your case and seeing your competing offers, we can offer $95,000 with the same benefits package.",
            "We appreciate your negotiation skills and transparency. We really want to make this work - what if we went to $100,000?",
            "I understand your position. Let me be frank - you're our top candidate and we're willing to be flexible. What's your target number?",
            "We value your expertise and the results you've delivered in the past. Let's find a number that works for both of us.",
            "You've been very persuasive. Let me present this final offer to leadership and get back to you with our best possible number."
        ]
        self.salary_progression = [85000, 87000, 90000, 90000, 90000, 95000, 100000, 100000, 100000, 100000, 100000]
    
    def respond(self, round_num):
        if round_num < len(self.responses):
            return self.responses[round_num], self.salary_progression[round_num]
        return "Thank you for your time. We'll be moving forward with other candidates. Best of luck with your job search.", 100000

def display_message(sender, message, message_type="system"):
    """Display a message in the chat interface"""
    if message_type == "negotiator":
        st.markdown(f"""
        <div class="bot-message negotiator-message">
            <strong>🤖 Negotiator Bot:</strong> {message}
        </div>
        """, unsafe_allow_html=True)
    elif message_type == "recruiter":
        st.markdown(f"""
        <div class="bot-message recruiter-message">
            <strong>💼 Recruiter Bot:</strong> {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-message system-message">
            <strong>ℹ️ System:</strong> {message}
        </div>
        """, unsafe_allow_html=True)

def display_typing_indicator(sender):
    """Display typing indicator"""
    if sender == "negotiator":
        st.markdown(f"""
        <div class="typing-indicator">
            🤖 Negotiator Bot is typing...
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="typing-indicator">
            💼 Recruiter Bot is typing...
        </div>
        """, unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Negotiator Bot vs Recruiter Bot</h1>
        <p>Watch AI-powered negotiation in action!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for controls
    with st.sidebar:
        st.header("🎛️ Controls")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key to enable AI-powered negotiation"
        )
        
        if api_key and not st.session_state.negotiator_bot:
            try:
                st.session_state.negotiator_bot = NegotiatorBot(api_key)
                st.success("✅ Negotiator Bot initialized!")
            except Exception as e:
                st.error(f"❌ Error initializing bot: {str(e)}")
        
        st.divider()
        
        # Start/Stop controls
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Start Negotiation", disabled=not st.session_state.negotiator_bot):
                st.session_state.conversation_active = True
                st.session_state.conversation_history = []
                st.session_state.round_count = 0
                st.session_state.current_salary = 85000
                
                # Initialize negotiator context
                if st.session_state.negotiator_bot:
                    user_profile = {
                        "years_experience": 5,
                        "industry": "technology",
                        "primary_skill": "software development",
                        "key_achievement": "led team that increased productivity by 40%",
                        "education_level": "Bachelors",
                        "leadership_experience": True,
                        "certifications": [],
                    }
                    
                    st.session_state.context_id = st.session_state.negotiator_bot.create_negotiation_context(
                        company_name="Tech Company",
                        position="Software Engineer II",
                        user_profile=user_profile,
                        target_salary=120000,
                        target_benefits=["health_insurance", "401k", "stock_options"],
                        deal_breakers=["no_remote_work", "salary_below_100k"]
                    )
                
                st.rerun()
        
        with col2:
            if st.button("⏹️ Stop", disabled=not st.session_state.conversation_active):
                st.session_state.conversation_active = False
                st.rerun()
        
        st.divider()
        
        # Statistics
        st.header("📊 Statistics")
        st.metric("Current Salary", f"${st.session_state.current_salary:,}")
        st.metric("Negotiation Rounds", st.session_state.round_count)
        st.metric("Salary Increase", f"${st.session_state.current_salary - 85000:,}")
        
        if st.session_state.current_salary > 85000:
            increase_percent = ((st.session_state.current_salary - 85000) / 85000) * 100
            st.metric("Increase %", f"{increase_percent:.1f}%")
    
    # Main chat area
    st.header("💬 Negotiation Chat")
    
    # Display conversation history
    chat_container = st.container()
    
    with chat_container:
        if not st.session_state.conversation_history:
            display_message("system", "Click 'Start Negotiation' to begin the AI-powered negotiation between the Negotiator Bot and Recruiter Bot!")
        else:
            for message in st.session_state.conversation_history:
                display_message(message['sender'], message['content'], message['type'])
    
    # Auto-negotiation logic
    if st.session_state.conversation_active and st.session_state.negotiator_bot:
        if st.session_state.round_count == 0:
            # Initial recruiter offer
            recruiter_bot = RecruiterBot()
            message, salary = recruiter_bot.respond(0)
            st.session_state.conversation_history.append({
                'sender': 'recruiter',
                'content': message,
                'type': 'recruiter',
                'timestamp': datetime.now()
            })
            st.session_state.current_salary = salary
            st.session_state.round_count = 1
            st.rerun()
        
        elif st.session_state.round_count < 10 and st.session_state.round_count % 2 == 1:
            # Negotiator's turn
            display_typing_indicator("negotiator")
            
            # Simulate thinking time
            time.sleep(2)
            
            try:
                # Generate negotiator response
                response = st.session_state.negotiator_bot.generate_response(
                    st.session_state.context_id,
                    "We need to discuss the compensation package.",
                    {"salary": st.session_state.current_salary}
                )
                
                st.session_state.conversation_history.append({
                    'sender': 'negotiator',
                    'content': response,
                    'type': 'negotiator',
                    'timestamp': datetime.now()
                })
                st.session_state.round_count += 1
                st.rerun()
                
            except Exception as e:
                st.error(f"Error generating negotiator response: {str(e)}")
                st.session_state.conversation_active = False
        
        elif st.session_state.round_count < 10 and st.session_state.round_count % 2 == 0:
            # Recruiter's turn
            display_typing_indicator("recruiter")
            
            # Simulate thinking time
            time.sleep(1.5)
            
            recruiter_bot = RecruiterBot()
            message, salary = recruiter_bot.respond(st.session_state.round_count // 2)
            
            st.session_state.conversation_history.append({
                'sender': 'recruiter',
                'content': message,
                'type': 'recruiter',
                'timestamp': datetime.now()
            })
            st.session_state.current_salary = salary
            st.session_state.round_count += 1
            st.rerun()
        
        else:
            # End of negotiation
            st.session_state.conversation_active = False
            display_message("system", f"Negotiation completed! Final salary: ${st.session_state.current_salary:,}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🤖 Powered by OpenAI GPT • Built with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
