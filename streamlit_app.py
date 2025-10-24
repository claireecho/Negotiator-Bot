import streamlit as st
import time
import json
from datetime import datetime
from main import NegotiatorBot, NegotiationStrategy, ResponseTone, NegotiationContext, ResponseTemplate
from offer_generator import OfferGenerator, CompanyType
from resume_parser import ResumeParser
from dataclasses import dataclass
from typing import List, Dict
import random
import tempfile
import os

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
if 'current_offer' not in st.session_state:
    st.session_state.current_offer = None
if 'offer_generator' not in st.session_state:
    st.session_state.offer_generator = OfferGenerator()
if 'resume_parser' not in st.session_state:
    st.session_state.resume_parser = ResumeParser()
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None

# Recruiter Bot Class
class RecruiterBot:
    def __init__(self, offer=None):
        self.offer = offer
        self.responses = [
            "Thank you for your interest in joining our team! After reviewing your application, we're pleased to extend you an offer for the {position} position. The salary is ${salary:,} with comprehensive benefits including {benefits}. This offer reflects our assessment of your qualifications and the market rate for this role. Do you have any questions about the offer?",
            "I understand your perspective, but our standard rate for this level is firm. We have many qualified candidates interested in this position.",
            "I appreciate your enthusiasm, but our budget is fixed for this role. We can offer additional benefits like flexible hours or professional development opportunities.",
            "We value your skills, but we need to maintain consistency across our team. Perhaps we can discuss a performance review after 6 months?",
            "I understand your concerns about market rates. Let me check with our compensation team and get back to you with a revised offer.",
            "We're excited about your potential, but we need to work within our established salary bands. Would you be open to discussing other forms of compensation?",
            "Thank you for your patience. After reviewing your case, we can offer ${salary:,} with the same benefits package. This is our final offer.",
            "We appreciate your negotiation skills, but we need to make a decision soon. We have other candidates waiting for our response.",
            "I understand your position, but we need to maintain fairness across our team. Our offer remains at ${salary:,}.",
            "We value your expertise, but we have budget constraints. Perhaps we can revisit this conversation in a few months?",
            "Thank you for your time. We'll be moving forward with other candidates. Best of luck with your job search."
        ]
        # Much more conservative salary progression
        self.salary_progression = [0, 0, 0, 1000, 2000, 3000, 5000, 5000, 5000, 5000, 5000]
    
    def respond(self, round_num):
        if self.offer is None:
            return "No offer available", 0
            
        base_salary = self.offer.base_salary
        difficulty = self.offer.negotiation_difficulty
        
        # Adjust salary progression based on difficulty
        if difficulty < 0.4:  # Easy companies
            progression = [0, 0, 1000, 2000, 3000, 4000, 5000, 5000, 5000, 5000, 5000]
        elif difficulty < 0.7:  # Medium companies
            progression = [0, 0, 0, 1000, 1500, 2500, 3000, 3000, 3000, 3000, 3000]
        else:  # Hard companies
            progression = [0, 0, 0, 0, 500, 1000, 1500, 1500, 1500, 1500, 1500]
        
        if round_num < len(progression):
            current_salary = base_salary + progression[round_num]
        else:
            current_salary = base_salary + progression[-1]
        
        # Add resistance based on difficulty and round
        if round_num < len(self.responses):
            # Show salary in response if it's the initial offer OR if it's actually an increase
            if round_num == 0 or current_salary > base_salary:
                response = self.responses[round_num].format(
                    position=self.offer.position,
                    salary=current_salary,
                    benefits=", ".join(self.offer.benefits[:3])  # Show first 3 benefits
                )
            else:
                # For other responses without increases, don't mention specific salary amounts
                response = self.responses[round_num]
                # Only replace salary if the response actually mentions a salary increase
                if "can offer" in response.lower() or "revised offer" in response.lower():
                    response = response.replace("{salary:,}", f"${current_salary:,}")
                elif "{salary:,}" in response:
                    # Remove salary mention for responses that don't represent increases
                    response = response.replace("{salary:,}", "our current offer")
                if "{position}" in response:
                    response = response.replace("{position}", self.offer.position)
                if "{benefits}" in response:
                    response = response.replace("{benefits}", ", ".join(self.offer.benefits[:3]))
            
            # Add resistance for hard companies
            if difficulty > 0.7 and round_num > 2:
                resistance_phrases = [
                    "I need to be clear - this is pushing our budget limits.",
                    "We have very strict compensation guidelines we must follow.",
                    "I'm not sure we can justify this increase to leadership.",
                    "This is significantly above our typical range for this role.",
                    "We need to maintain equity across our team members."
                ]
                if round_num % 2 == 0:  # Every other response
                    response += f" {random.choice(resistance_phrases)}"
            
            return response, current_salary
        return "Thank you for your time. We'll be moving forward with other candidates. Best of luck with your job search.", current_salary

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
        
        # Resume Upload Section
        st.header("📄 Resume Upload")
        
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF, DOCX, or TXT)",
            type=['pdf', 'docx', 'txt'],
            help="Upload your resume to personalize the negotiation with your actual experience and skills"
        )
        
        if uploaded_file is not None:
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                # Parse resume
                file_type = uploaded_file.name.split('.')[-1]
                resume_data = st.session_state.resume_parser.parse_resume(tmp_file_path, file_type)
                st.session_state.resume_data = resume_data
                
                # Clean up temp file
                os.unlink(tmp_file_path)
                
                st.success("✅ Resume parsed successfully! Your negotiation will now be personalized based on your experience and skills.")
                
            except Exception as e:
                st.error(f"❌ Error parsing resume: {str(e)}")
                st.session_state.resume_data = None
        
        elif st.session_state.resume_data is None:
            st.info("💡 Upload your resume to get personalized negotiation responses based on your actual experience and skills!")
        
        st.divider()
        
        # Offer Selection
        st.header("🎯 Job Offer Selection")
        
        # Company type filter
        company_type = st.selectbox(
            "Company Type",
            ["Random", "Tech Giant", "Startup", "Finance", "Consulting", "Healthcare", "Automotive", "Retail", "Media"],
            help="Select the type of company for the job offer"
        )
        
        # Generate new offer button
        if st.button("🎲 Generate New Offer", help="Generate a random job offer"):
            try:
                if company_type == "Random":
                    st.session_state.current_offer = st.session_state.offer_generator.generate_offer()
                else:
                    company_type_enum = CompanyType(company_type.lower().replace(" ", "_"))
                    st.session_state.current_offer = st.session_state.offer_generator.generate_offer(company_type_enum)
                st.rerun()
            except Exception as e:
                st.error(f"Error generating offer: {str(e)}")
        
        # Display current offer
        if st.session_state.current_offer:
            offer = st.session_state.current_offer
            st.markdown("### 📋 Current Offer")
            st.markdown(f"**🏢 Company:** {offer.company_name}")
            st.markdown(f"**💼 Position:** {offer.position}")
            st.markdown(f"**💰 Base Salary:** ${offer.base_salary:,}")
            st.markdown(f"**📍 Location:** {offer.location}")
            st.markdown(f"**🏢 Size:** {offer.company_size}")
            st.markdown(f"**📊 Difficulty:** {'Easy' if offer.negotiation_difficulty < 0.4 else 'Medium' if offer.negotiation_difficulty < 0.7 else 'Hard'}")
            
            with st.expander("📝 Full Details"):
                st.markdown(f"**Description:** {offer.description}")
                st.markdown("**Benefits:**")
                for benefit in offer.benefits:
                    st.markdown(f"• {benefit}")
        else:
            st.info("Click 'Generate New Offer' to create a job offer for negotiation")
        
        st.divider()
        
        # Start/Stop controls
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Start Negotiation", disabled=not st.session_state.negotiator_bot or not st.session_state.current_offer):
                st.session_state.conversation_active = True
                st.session_state.conversation_history = []
                st.session_state.round_count = 0
                st.session_state.current_salary = st.session_state.current_offer.base_salary
                
                # Initialize negotiator context
                if st.session_state.negotiator_bot:
                    if st.session_state.resume_data:
                        # Use resume data for personalized context
                        user_profile = st.session_state.resume_parser.get_negotiation_context(st.session_state.resume_data)
                    else:
                        # Default profile if no resume uploaded
                        user_profile = {
                            "name": "Candidate",
                            "years_experience": 5,
                            "industry": "technology",
                            "primary_skill": "software development",
                            "key_achievement": "led team that increased productivity by 40%",
                            "education_level": "Bachelors",
                            "leadership_experience": True,
                            "certifications": [],
                            "current_title": "Software Engineer",
                            "current_company": "Tech Company",
                            "summary": "Experienced software engineer with strong technical skills"
                        }
                    
                    st.session_state.context_id = st.session_state.negotiator_bot.create_negotiation_context(
                        company_name=st.session_state.current_offer.company_name,
                        position=st.session_state.current_offer.position,
                        user_profile=user_profile,
                        target_salary=int(st.session_state.current_offer.base_salary * 1.2),  # 20% above offer
                        target_benefits=st.session_state.current_offer.benefits,
                        deal_breakers=["no_remote_work", f"salary_below_{st.session_state.current_offer.base_salary}"]
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
    if st.session_state.conversation_active and st.session_state.negotiator_bot and st.session_state.current_offer:
        if st.session_state.round_count == 0:
            # Initial recruiter offer
            recruiter_bot = RecruiterBot(st.session_state.current_offer)
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
            
            recruiter_bot = RecruiterBot(st.session_state.current_offer)
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
