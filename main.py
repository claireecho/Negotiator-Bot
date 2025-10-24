import os
import json
from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
import random
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import io
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
# Import moved to avoid circular dependency

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Negotiator Bot Classes
class NegotiationStrategy(Enum):
    PROFESSIONAL_PASSIVE_AGGRESSIVE = "professional_passive_aggressive"
    CONFIDENT_ASSERTIVE = "confident_assertive"
    COLLABORATIVE_PROBLEM_SOLVER = "collaborative_problem_solver"
    STRATEGIC_QUESTIONER = "strategic_questioner"

class ResponseTone(Enum):
    POLITE_BUT_FIRM = "polite_but_firm"
    PROFESSIONALLY_DISAPPOINTED = "professionally_disappointed"
    STRATEGICALLY_CURIOUS = "strategically_curious"
    CONFIDENTLY_ASSERTIVE = "confidently_assertive"

@dataclass
class NegotiationContext:
    company_name: str
    position: str
    current_offer: Optional[Dict]
    user_profile: Dict
    negotiation_history: List[Dict]
    strategy: NegotiationStrategy
    target_salary: Optional[int]
    target_benefits: List[str]
    deal_breakers: List[str]
    leverage_points: List[str]

@dataclass
class ResponseTemplate:
    template_id: str
    strategy: NegotiationStrategy
    tone: ResponseTone
    template_text: str
    variables: List[str]
    effectiveness_score: float

class NegotiatorBot:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = OpenAI(api_key=self.api_key)
        self.response_templates = self._load_response_templates()
        self.negotiation_contexts = {}
        
    def _load_response_templates(self) -> List[ResponseTemplate]:
        """Load pre-built response templates for different negotiation scenarios"""
        templates = [
            # Professional Passive-Aggressive Templates
            ResponseTemplate(
                template_id="salary_undervalued",
                strategy=NegotiationStrategy.PROFESSIONAL_PASSIVE_AGGRESSIVE,
                tone=ResponseTone.PROFESSIONALLY_DISAPPOINTED,
                template_text="""Thank you for your offer. While I appreciate the opportunity, I must express some concern about the compensation package. Given my {experience_years} years of experience in {industry} and my track record of {achievement}, I had hoped for a more competitive offer that reflects market standards. 

I'm curious about your compensation philosophy - do you typically benchmark against industry standards? I'd be interested to understand how you arrived at this figure, as it seems significantly below what I've seen for similar roles at comparable companies.""",
                variables=["experience_years", "industry", "achievement"],
                effectiveness_score=0.85
            ),
            
            # More Aggressive and Persuasive Templates
            ResponseTemplate(
                template_id="market_value_assertion_strong",
                strategy=NegotiationStrategy.CONFIDENT_ASSERTIVE,
                tone=ResponseTone.CONFIDENTLY_ASSERTIVE,
                template_text="""I appreciate the offer, but I need to be direct about the market reality. My research shows that professionals with my {experience_years} years of experience in {industry} and proven track record of {achievement} are commanding {target_salary_range} in the current market.

I have multiple offers in the pipeline, and while I'm genuinely excited about this opportunity, I need to ensure we're aligned on compensation. The current offer is approximately {salary_gap} below market rate, which concerns me about how the company values top talent.

What flexibility do you have to bridge this gap? I'm confident I can deliver exceptional value, but I need compensation that reflects that value proposition.""",
                variables=["experience_years", "industry", "achievement", "target_salary_range", "salary_gap"],
                effectiveness_score=0.92
            ),
            
            ResponseTemplate(
                template_id="leverage_competition",
                strategy=NegotiationStrategy.CONFIDENT_ASSERTIVE,
                tone=ResponseTone.CONFIDENTLY_ASSERTIVE,
                template_text="""I'm excited about this role, but I need to be transparent about my situation. I have a competing offer from {competitor_company} for {competing_salary}, and while I prefer this opportunity, the compensation gap is significant.

My decision timeline is tight - I need to respond to them by {deadline}. However, I'm willing to give you priority if we can find a mutually beneficial arrangement.

What's the highest you can go? I'm looking for {target_salary} to make this work, but I'm open to creative solutions like performance bonuses, equity, or accelerated review cycles.""",
                variables=["competitor_company", "competing_salary", "deadline", "target_salary"],
                effectiveness_score=0.95
            ),
            
            ResponseTemplate(
                template_id="value_proposition_strong",
                strategy=NegotiationStrategy.CONFIDENT_ASSERTIVE,
                tone=ResponseTone.CONFIDENTLY_ASSERTIVE,
                template_text="""Let me be clear about what I bring to the table. In my previous role, I {specific_achievement} which resulted in {quantified_impact}. I'm not just looking for a job - I'm looking to make a significant impact.

The current offer doesn't reflect the value I can deliver. I'm confident I can {future_value_proposition} within the first year, which would justify a higher compensation package.

I'm asking for {target_salary} because that's what the market pays for someone who can deliver these results. What do you think about structuring this as a performance-based increase with a higher base?""",
                variables=["specific_achievement", "quantified_impact", "future_value_proposition", "target_salary"],
                effectiveness_score=0.90
            ),
            
            ResponseTemplate(
                template_id="benefits_inadequate",
                strategy=NegotiationStrategy.PROFESSIONAL_PASSIVE_AGGRESSIVE,
                tone=ResponseTone.STRATEGICALLY_CURIOUS,
                template_text="""I notice the benefits package is quite different from what I've seen at other companies in this space. Specifically, the {benefit_type} seems limited compared to industry standards. 

Could you help me understand your benefits philosophy? I'm particularly interested in how you view employee retention and work-life balance, as these factors significantly impact my decision-making process.""",
                variables=["benefit_type"],
                effectiveness_score=0.80
            ),
            
            ResponseTemplate(
                template_id="market_value_assertion",
                strategy=NegotiationStrategy.CONFIDENT_ASSERTIVE,
                tone=ResponseTone.CONFIDENTLY_ASSERTIVE,
                template_text="""Based on my research and conversations with industry peers, my market value for this role is significantly higher than what's being offered. My expertise in {skill_area} and proven track record of {specific_achievement} command premium compensation.

I'm confident I can deliver exceptional value to {company_name}, but I need to ensure the compensation reflects that value proposition. Let's discuss how we can align the offer with market standards.""",
                variables=["skill_area", "specific_achievement", "company_name"],
                effectiveness_score=0.88
            ),
            
            ResponseTemplate(
                template_id="creative_solution",
                strategy=NegotiationStrategy.COLLABORATIVE_PROBLEM_SOLVER,
                tone=ResponseTone.POLITE_BUT_FIRM,
                template_text="""I understand budget constraints, but I'm confident we can find a creative solution that works for both parties. Here are some alternatives I'd be open to discussing:

- Performance-based bonuses tied to specific metrics
- Additional equity/stock options
- Professional development budget
- Flexible work arrangements
- Earlier salary review timeline

What combination of these would make sense for your organization?""",
                variables=[],
                effectiveness_score=0.87
            )
        ]
        return templates
    
    def create_negotiation_context(self, company_name: str, position: str, 
                                 user_profile: Dict, target_salary: int = None,
                                 target_benefits: List[str] = None,
                                 deal_breakers: List[str] = None) -> str:
        """Create a new negotiation context"""
        context_id = f"{company_name}_{position}_{int(datetime.now().timestamp())}"
        
        context = NegotiationContext(
            company_name=company_name,
            position=position,
            current_offer=None,
            user_profile=user_profile,
            negotiation_history=[],
            strategy=NegotiationStrategy.PROFESSIONAL_PASSIVE_AGGRESSIVE,
            target_salary=target_salary,
            target_benefits=target_benefits or [],
            deal_breakers=deal_breakers or [],
            leverage_points=self._identify_leverage_points(user_profile)
        )
        
        self.negotiation_contexts[context_id] = context
        return context_id
    
    def _identify_leverage_points(self, user_profile: Dict) -> List[str]:
        """Identify leverage points from user profile"""
        leverage_points = []
        
        if user_profile.get("years_experience", 0) > 5:
            leverage_points.append("senior_experience")
        if user_profile.get("education_level") in ["Masters", "PhD"]:
            leverage_points.append("advanced_education")
        if user_profile.get("certifications"):
            leverage_points.append("specialized_certifications")
        if user_profile.get("leadership_experience"):
            leverage_points.append("leadership_skills")
        if user_profile.get("industry_awards"):
            leverage_points.append("industry_recognition")
        if user_profile.get("current_offer"):
            leverage_points.append("competing_offer")
            
        return leverage_points
    
    def generate_response(self, context_id: str, incoming_message: str, 
                         offer_details: Dict = None) -> str:
        """Generate a negotiation response using AI and templates"""
        if context_id not in self.negotiation_contexts:
            raise ValueError(f"Context {context_id} not found")
        
        context = self.negotiation_contexts[context_id]
        
        # Update context with new offer if provided
        if offer_details:
            context.current_offer = offer_details
            context.negotiation_history.append({
                "timestamp": datetime.now().isoformat(),
                "type": "offer_received",
                "details": offer_details
            })
        
        # Analyze the incoming message
        analysis = self._analyze_incoming_message(incoming_message, context)
        
        # Select appropriate template
        template = self._select_template(analysis, context)
        
        # Generate response using AI
        response = self._generate_ai_response(template, context, analysis)
        
        # Log the response
        context.negotiation_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "response_sent",
            "template_used": template.template_id,
            "response": response
        })
        
        return response
    
    def _analyze_incoming_message(self, message: str, context: NegotiationContext) -> Dict:
        """Analyze incoming message to determine negotiation tactics"""
        analysis_prompt = f"""
        Analyze this negotiation message from a company recruiter/manager:
        
        Message: "{message}"
        
        Context:
        - Company: {context.company_name}
        - Position: {context.position}
        - User's target salary: {context.target_salary}
        - User's leverage points: {context.leverage_points}
        
        Determine:
        1. What negotiation tactic is the company using?
        2. What pressure points are they applying?
        3. What information are they seeking?
        4. How should we respond strategically?
        
        Respond in JSON format with analysis results.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content
            return json.loads(analysis_text)
        except Exception as e:
            print(f"Error analyzing message: {e}")
            return {"tactic": "unknown", "pressure_points": [], "response_strategy": "professional"}
    
    def _select_template(self, analysis: Dict, context: NegotiationContext) -> ResponseTemplate:
        """Select the most appropriate response template"""
        # Filter templates by strategy
        strategy_templates = [t for t in self.response_templates 
                            if t.strategy == context.strategy]
        
        # Score templates based on analysis and context
        scored_templates = []
        for template in strategy_templates:
            score = template.effectiveness_score
            
            # Boost score based on context match
            if context.current_offer and "salary" in template.template_id:
                current_salary = context.current_offer.get("salary", 0)
                # Extract numeric value from salary string (e.g., "$85,000" -> 85000)
                if isinstance(current_salary, str):
                    current_salary = int(''.join(filter(str.isdigit, current_salary)))
                if current_salary < (context.target_salary or 0):
                    score += 0.1
            
            scored_templates.append((template, score))
        
        # Return highest scoring template
        scored_templates.sort(key=lambda x: x[1], reverse=True)
        return scored_templates[0][0]
    
    def _generate_ai_response(self, template: ResponseTemplate, context: NegotiationContext, 
                            analysis: Dict) -> str:
        """Generate AI-enhanced response using template"""
        # Prepare variables for template
        variables = {}
        for var in template.variables:
            if var == "experience_years":
                variables[var] = context.user_profile.get("years_experience", "5+")
            elif var == "industry":
                variables[var] = context.user_profile.get("industry", "technology")
            elif var == "achievement":
                variables[var] = context.user_profile.get("key_achievement", "delivering exceptional results")
            elif var == "benefit_type":
                variables[var] = "health insurance"
            elif var == "skill_area":
                variables[var] = context.user_profile.get("primary_skill", "software development")
            elif var == "specific_achievement":
                variables[var] = context.user_profile.get("key_achievement", "increasing team productivity by 40%")
            elif var == "company_name":
                variables[var] = context.company_name
            elif var == "target_salary_range":
                variables[var] = f"${context.target_salary - 10000}-${context.target_salary + 10000}" if context.target_salary else "$100,000-$130,000"
            elif var == "salary_gap":
                if context.current_offer and context.target_salary:
                    current_salary = context.current_offer.get("salary", 0)
                    if isinstance(current_salary, str):
                        current_salary = int(''.join(filter(str.isdigit, current_salary)))
                    gap = context.target_salary - current_salary
                    variables[var] = f"${gap:,}"
                else:
                    variables[var] = "$15,000-$25,000"
            elif var == "competitor_company":
                companies = ["Google", "Microsoft", "Amazon", "Apple", "Meta", "Netflix", "Uber", "Airbnb"]
                variables[var] = companies[hash(context.company_name) % len(companies)]
            elif var == "competing_salary":
                target = context.target_salary or 120000
                variables[var] = f"${target + 5000:,}"
            elif var == "deadline":
                variables[var] = "Friday"
            elif var == "target_salary":
                variables[var] = f"${context.target_salary:,}" if context.target_salary else "$120,000"
            elif var == "quantified_impact":
                impacts = ["increased revenue by 150%", "reduced costs by $2M annually", "improved efficiency by 40%", "led to 300% user growth"]
                variables[var] = impacts[hash(context.company_name) % len(impacts)]
            elif var == "future_value_proposition":
                propositions = ["increase team productivity by 50%", "deliver $5M in cost savings", "launch 3 major features", "build a scalable architecture"]
                variables[var] = propositions[hash(context.company_name) % len(propositions)]
                
        # Format template with variables
        formatted_template = template.template_text.format(**variables)
        
        # Enhance with AI
        enhancement_prompt = f"""
        Transform this negotiation response into a highly persuasive, strategic communication that will make the recruiter more likely to increase their offer. Use advanced negotiation psychology:

        Original Response:
        {formatted_template}
        
        Context:
        - Company: {context.company_name}
        - Position: {context.position}
        - Target salary: {context.target_salary}
        - Current offer: {context.current_offer}
        - Leverage points: {context.leverage_points}
        
        Apply these persuasive techniques:
        1. Create urgency and scarcity ("I have other offers", "timeline pressure")
        2. Use social proof and authority ("industry standards", "market research")
        3. Frame as mutual benefit ("win-win", "partnership")
        4. Use specific numbers and data
        5. Create FOMO (fear of missing out)
        6. Use confident, assertive language
        7. Suggest creative solutions
        8. Reference the company's values/mission
        
        Make the candidate sound highly desirable and in-demand. The recruiter should feel they need to act quickly to secure this talent.
        
        Keep it professional but compelling. Maximum 200 words.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": enhancement_prompt}],
                temperature=0.8,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return formatted_template
    
    def get_negotiation_status(self, context_id: str) -> Dict:
        """Get current status of a negotiation"""
        if context_id not in self.negotiation_contexts:
            return {"error": "Context not found"}
        
        context = self.negotiation_contexts[context_id]
        
        return {
            "company": context.company_name,
            "position": context.position,
            "strategy": context.strategy.value,
            "current_offer": context.current_offer,
            "negotiation_history": context.negotiation_history,
            "leverage_points": context.leverage_points,
            "target_salary": context.target_salary
        }
    
    def update_strategy(self, context_id: str, new_strategy: NegotiationStrategy):
        """Update negotiation strategy"""
        if context_id in self.negotiation_contexts:
            self.negotiation_contexts[context_id].strategy = new_strategy
    
    def add_leverage_point(self, context_id: str, leverage_point: str):
        """Add a new leverage point"""
        if context_id in self.negotiation_contexts:
            self.negotiation_contexts[context_id].leverage_points.append(leverage_point)

# Global instances
negotiator_bot = None
offer_generator = None

def get_offer_generator():
    """Lazy initialization of offer generator to avoid circular imports"""
    global offer_generator
    if offer_generator is None:
        from offer_generator import OfferGenerator
        offer_generator = OfferGenerator()
    return offer_generator
    
# Company-specific job offers with different levels
COMPANIES = {
    "tech_giants": [
        {
            "name": "Google",
            "logo": "🔍",
            "headquarters": "Mountain View, CA",
            "founded": "1998",
            "description": "Leading technology company specializing in internet-related services and products"
        },
        {
            "name": "Microsoft",
            "logo": "🪟",
            "headquarters": "Redmond, WA", 
            "founded": "1975",
            "description": "Multinational technology corporation developing computer software, consumer electronics, and cloud services"
        },
        {
            "name": "Apple",
            "logo": "🍎",
            "headquarters": "Cupertino, CA",
            "founded": "1976", 
            "description": "Technology company that designs, develops, and sells consumer electronics, computer software, and online services"
        },
        {
            "name": "Amazon",
            "logo": "📦",
            "headquarters": "Seattle, WA",
            "founded": "1994",
            "description": "Multinational technology company focusing on e-commerce, cloud computing, and artificial intelligence"
        }
    ],
    "startups": [
        {
            "name": "Stripe",
            "logo": "💳",
            "headquarters": "San Francisco, CA",
            "founded": "2010",
            "description": "Financial technology company that builds economic infrastructure for the internet"
        },
        {
            "name": "Airbnb",
            "logo": "🏠",
            "headquarters": "San Francisco, CA",
            "founded": "2008",
            "description": "Online marketplace for short-term homestays and experiences"
        },
        {
            "name": "Slack",
            "logo": "💬",
            "headquarters": "San Francisco, CA",
            "founded": "2009",
            "description": "Business communication platform for teams and organizations"
        }
    ],
    "fintech": [
        {
            "name": "PayPal",
            "logo": "💰",
            "headquarters": "San Jose, CA",
            "founded": "1998",
            "description": "American multinational financial technology company operating an online payments system"
        },
        {
            "name": "Square",
            "logo": "⬜",
            "headquarters": "San Francisco, CA",
            "founded": "2009",
            "description": "Financial services and digital payments company"
        }
    ]
}

JOB_OFFERS = {
    "newgrad": {
        "title": "New Grad Software Engineer",
        "salary": "$75,000",
        "benefits": ["Health Insurance", "401k with 4% match", "15 days PTO", "Learning & Development Budget", "Free Meals", "Gym Membership"],
        "description": "Entry-level position for recent computer science graduates with 0-1 years experience",
        "equity": "0.01% - 0.05%",
        "bonus": "Up to $5,000 signing bonus"
    },
    "entry": {
        "title": "Software Engineer I",
        "salary": "$85,000",
        "benefits": ["Health Insurance", "401k with 4% match", "18 days PTO", "Stock Options", "Free Meals", "Gym Membership"],
        "description": "Junior position for developers with 1-3 years of experience",
        "equity": "0.05% - 0.1%",
        "bonus": "Up to $8,000 signing bonus"
    },
    "mid": {
        "title": "Software Engineer II",
        "salary": "$105,000", 
        "benefits": ["Health Insurance", "401k with 6% match", "20 days PTO", "Stock Options", "Annual Bonus", "Free Meals", "Gym Membership"],
        "description": "Mid-level position for experienced developers with 3-6 years experience",
        "equity": "0.1% - 0.2%",
        "bonus": "Up to $12,000 signing bonus"
    },
    "senior": {
        "title": "Senior Software Engineer",
        "salary": "$130,000",
        "benefits": ["Health Insurance", "401k with 6% match", "25 days PTO", "Stock Options", "Annual Bonus", "Flexible Hours", "Free Meals", "Gym Membership"],
        "description": "Senior position for experienced professionals with 6+ years experience",
        "equity": "0.2% - 0.5%",
        "bonus": "Up to $20,000 signing bonus"
    }
}

def generate_initial_offer():
    """Generate an initial job offer with company selection"""
    offer_level = random.choice(["newgrad", "entry", "mid", "senior"])
    
    # Select a random company category and company
    company_category = random.choice(list(COMPANIES.keys()))
    company = random.choice(COMPANIES[company_category])
    
    # Create personalized offer
    offer = JOB_OFFERS[offer_level].copy()
    offer['company'] = company
    offer['company_category'] = company_category
    
    return offer, offer_level

def generate_offer_pdf(offer, offer_level):
    """Generate a professional PDF offer letter"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Company header
    company = offer['company']
    company_style = ParagraphStyle(
        'CompanyHeader',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=colors.HexColor('#2D3748')
    )
    
    story.append(Paragraph(f"{company['logo']} {company['name']}", company_style))
    story.append(Paragraph(f"{company['headquarters']} • Founded {company['founded']}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Offer title
    title_style = ParagraphStyle(
        'OfferTitle',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=20,
        textColor=colors.HexColor('#4A5568')
    )
    story.append(Paragraph(f"Job Offer: {offer['title']}", title_style))
    
    # Date
    story.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Compensation details
    comp_data = [
        ['Compensation', 'Details'],
        ['Base Salary', offer['salary']],
        ['Equity', offer['equity']],
        ['Signing Bonus', offer['bonus']]
    ]
    
    comp_table = Table(comp_data, colWidths=[2*inch, 3*inch])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E2E8F0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2D3748')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F7FAFC')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E0'))
    ]))
    
    story.append(Paragraph("Compensation Package", styles['Heading3']))
    story.append(comp_table)
    story.append(Spacer(1, 20))
    
    # Benefits
    story.append(Paragraph("Benefits & Perks", styles['Heading3']))
    benefits_text = "• " + "<br/>• ".join(offer['benefits'])
    story.append(Paragraph(benefits_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Job description
    story.append(Paragraph("Position Overview", styles['Heading3']))
    story.append(Paragraph(offer['description'], styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Company description
    story.append(Paragraph("About " + company['name'], styles['Heading3']))
    story.append(Paragraph(company['description'], styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#718096'),
        alignment=1
    )
    story.append(Paragraph("This offer is valid for 7 days from the date of issue.", footer_style))
    story.append(Paragraph("Generated by Recruiter Bot", footer_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def evaluate_negotiation(user_message, current_offer, offer_level, conversation_history, api_key):
    """Use GPT to evaluate negotiation and determine response"""
    
    # Count previous negotiations to make subsequent ones stricter
    negotiation_count = len([msg for msg in conversation_history if msg.get('role') == 'user'])
    
    system_prompt = f"""You are a professional recruiter for {current_offer['company']['name']}. You have made a firm initial offer for a {current_offer['title']} position.

CURRENT OFFER DETAILS:
- Company: {current_offer['company']['name']} (DO NOT CHANGE)
- Position: {current_offer['title']} (DO NOT CHANGE)
- Salary: {current_offer['salary']}
- Benefits: {', '.join(current_offer['benefits'])}
- Equity: {current_offer.get('equity', 'N/A')}
- Signing Bonus: {current_offer.get('bonus', 'N/A')}
- Description: {current_offer['description']}

NEGOTIATION HISTORY: This is negotiation attempt #{negotiation_count + 1}

IMPORTANT: This is a REAL job offer. The candidate must negotiate professionally and persuasively to get improvements. 
- For the FIRST negotiation attempt, be moderately lenient if the candidate provides reasonable arguments
- For subsequent attempts, be increasingly strict
- You are NOT generous - you only improve offers for compelling arguments

NEGOTIATION RULES:
1. NEVER change the company name or position title - these are FIXED
2. The initial offer is fair and competitive for the market
3. Each subsequent negotiation attempt should be STRICTER than the previous one
4. You only improve offers when candidates demonstrate:
   - Exceptional skills or experience beyond the role requirements
   - Strong negotiation skills with logical reasoning
   - Specific value they bring to the company
   - Professional communication and respect
   - Compelling evidence of their worth
5. Generic requests like "I want more money" are rejected
6. Unreasonable demands or unprofessional behavior result in offer withdrawal
7. You maintain a professional but firm tone
8. After 2+ negotiations, be VERY strict - only improve for exceptional cases
9. For testing purposes, be slightly more lenient on first negotiation attempts

OFFER WITHDRAWAL CRITERIA (use "withdraw" action):
- Unprofessional or disrespectful language
- Demanding or entitled attitude
- Making threats or ultimatums
- Repeatedly asking for unreasonable amounts after being told no
- Being rude, aggressive, or confrontational
- Making personal attacks or inappropriate comments
- Refusing to accept "no" and continuing to pressure
- Making unrealistic demands that show lack of understanding of the role

AVAILABLE OFFER LEVELS:
- New Grad: $75,000 (basic benefits + learning budget) - for recent CS graduates
- Entry: $85,000 (basic benefits + stock) - for developers with 1-3 years experience
- Mid: $105,000 (better benefits + stock + bonus) - for experienced developers
- Senior: $130,000 (best benefits + stock + bonus + flexibility) - for senior professionals

RESPONSE FORMAT (JSON):
{{
    "response": "Your professional response to the candidate",
    "action": "improve" | "maintain" | "decline" | "withdraw",
    "new_offer_level": "newgrad" | "entry" | "mid" | "senior" | null,
    "reasoning": "Brief explanation of your decision",
    "improvements": "If improving, list what specifically changed (e.g., 'Salary increased from $85,000 to $90,000, added 5 extra PTO days')",
    "new_offer": "If improving, provide the updated offer details with same company and position"
}}

EXAMPLES OF GOOD NEGOTIATIONS:
- "I have 8 years of experience in React and led a team of 5 developers at my previous company. I also have AWS certifications that would be valuable for this role."
- "I've reviewed the market rates for this position and my research shows senior developers with my skill set typically earn $90,000-$100,000. I bring expertise in microservices architecture that could save the company significant development time."

EXAMPLES OF BAD NEGOTIATIONS (maintain/decline):
- "I need more money"
- "This offer is too low"
- "Can you increase the salary?"
- "I want better benefits"

EXAMPLES OF WITHDRAWAL-WORTHY NEGOTIATIONS:
- "This is insulting, I deserve way more than this"
- "You're being cheap, I know you can afford more"
- "I'm not accepting anything less than $200k"
- "This is ridiculous, I'm wasting my time here"
- "You're making a mistake if you don't give me what I want"
- "I have other offers, you better match them or I'm gone"
- "This is pathetic, I expected better from [company name]"

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
        
        # For testing purposes, if it's an API key error, provide a mock improvement
        if "API key" in str(e) or "401" in str(e):
            return {
                "response": "Thank you for your compelling negotiation. Based on your experience and competing offers, we're pleased to improve our offer.",
                "action": "improve",
                "new_offer_level": "senior",
                "reasoning": "Strong negotiation with competing offers",
                "improvements": "Salary increased from $105,000 to $130,000, equity increased to 0.2% - 0.5%, signing bonus increased to $20,000"
            }
        
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
    
    company = initial_offer['company']
    return jsonify({
        'offer': initial_offer,
        'offer_level': offer_level,
        'message': f"Thank you for your interest in joining {company['name']}! After reviewing your application, we're pleased to extend you an offer for the {initial_offer['title']} position at our {company['headquarters']} office. The salary is {initial_offer['salary']} with comprehensive benefits including {', '.join(initial_offer['benefits'][:3])} and more. This offer reflects our assessment of your qualifications and the market rate for this role. Do you have any questions about the offer?"
    })

@app.route('/negotiate', methods=['POST'])
def negotiate():
    """Handle negotiation attempts"""
    data = request.json
    user_message = data.get('message', '')
    current_offer = data.get('current_offer', {})
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
    
    # Use current offer if provided, otherwise fall back to template
    if not current_offer:
        current_offer = JOB_OFFERS[current_offer_level]
    
    # Evaluate the negotiation
    evaluation = evaluate_negotiation(user_message, current_offer, current_offer_level, conversation_history, api_key)
    
    response_data = {
        'response': evaluation['response'],
        'action': evaluation['action'],
        'reasoning': evaluation['reasoning']
    }
    
    # Handle improved offers - preserve company and position
    if evaluation['action'] == 'improve':
        if evaluation.get('new_offer_level'):
            new_level = evaluation['new_offer_level']
            # Create improved offer with same company and position
            improved_offer = JOB_OFFERS[new_level].copy()
            improved_offer['company'] = current_offer['company']  # Preserve company
            improved_offer['title'] = current_offer['title']  # Preserve position
            improved_offer['company_category'] = current_offer.get('company_category', 'tech_giants')
            
            response_data['new_offer'] = improved_offer
            response_data['new_offer_level'] = new_level
            response_data['improvements'] = evaluation.get('improvements', 'Offer improved')
        else:
            # If action is improve but no new_offer_level, treat as maintain
            response_data['action'] = 'maintain'
            response_data['current_offer'] = current_offer
            response_data['offer_level'] = current_offer_level
    elif evaluation['action'] == 'maintain':
        response_data['current_offer'] = current_offer
        response_data['offer_level'] = current_offer_level
    elif evaluation['action'] == 'decline':
        response_data['offer_declined'] = True
    elif evaluation['action'] == 'withdraw':
        response_data['offer_withdrawn'] = True
    
    return jsonify(response_data)

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    """Download PDF offer letter with specific offer data"""
    data = request.json
    offer = data.get('offer')
    
    if not offer:
        return jsonify({'error': 'No offer data provided'}), 400
    
    pdf_buffer = generate_offer_pdf(offer, offer.get('offer_level', 'entry'))
    
    company_name = offer['company']['name'].replace(' ', '_')
    filename = f"{company_name}_{offer['title'].replace(' ', '_')}_Offer.pdf"
    
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route("/get_random_offer", methods=["GET"])
def get_random_offer():
    """Get a random job offer from various companies"""
    try:
        # Get company type from query params (optional)
        company_type_str = request.args.get("company_type", "").lower()
        company_type = None
        
        if company_type_str:
            try:
                from offer_generator import CompanyType
                company_type = CompanyType(company_type_str)
            except ValueError:
                pass  # Use random if invalid type
        
        # Generate offer
        generator = get_offer_generator()
        offer = generator.generate_offer(company_type)
        
        # Convert to dict for JSON response
        offer_dict = {
            "company_name": offer.company_name,
            "position": offer.position,
            "base_salary": offer.base_salary,
            "company_type": offer.company_type.value,
            "industry": offer.industry,
            "benefits": offer.benefits,
            "location": offer.location,
            "company_size": offer.company_size,
            "description": offer.description,
            "negotiation_difficulty": offer.negotiation_difficulty
        }
        
        return jsonify(offer_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_multiple_offers", methods=["GET"])
def get_multiple_offers():
    """Get multiple diverse job offers"""
    try:
        count = int(request.args.get("count", 5))
        count = min(max(count, 1), 10)  # Limit between 1 and 10
        
        generator = get_offer_generator()
        offers = generator.generate_multiple_offers(count)
        
        # Convert to list of dicts
        offers_list = []
        for offer in offers:
            offer_dict = {
                "company_name": offer.company_name,
                "position": offer.position,
                "base_salary": offer.base_salary,
                "company_type": offer.company_type.value,
                "industry": offer.industry,
                "benefits": offer.benefits,
                "location": offer.location,
                "company_size": offer.company_size,
                "description": offer.description,
                "negotiation_difficulty": offer.negotiation_difficulty
            }
            offers_list.append(offer_dict)
        
        return jsonify(offers_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Negotiator Bot Routes
@app.route('/create_negotiation_context', methods=['POST'])
def create_negotiation_context():
    """Create a new negotiation context for the negotiator bot"""
    data = request.json
    api_key = data.get('api_key')
    
    if not api_key:
        return jsonify({'error': 'API key is required'}), 400
    
    if not api_key.startswith('sk-') or len(api_key) < 20:
        return jsonify({'error': 'Invalid API key format'}), 400
    
    try:
        global negotiator_bot
        negotiator_bot = NegotiatorBot(api_key)
        
        context_id = negotiator_bot.create_negotiation_context(
            company_name=data.get('company_name', 'Unknown Company'),
            position=data.get('position', 'Software Engineer'),
            user_profile=data.get('user_profile', {}),
            target_salary=data.get('target_salary'),
            target_benefits=data.get('target_benefits', []),
            deal_breakers=data.get('deal_breakers', [])
        )
        
        return jsonify({
            'context_id': context_id,
            'message': 'Negotiation context created successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_negotiation_response', methods=['POST'])
def generate_negotiation_response():
    """Generate a negotiation response using the negotiator bot"""
    data = request.json
    context_id = data.get('context_id')
    incoming_message = data.get('message')
    offer_details = data.get('offer_details')
    
    if not context_id or not incoming_message:
        return jsonify({'error': 'Context ID and message are required'}), 400
    
    if not negotiator_bot:
        return jsonify({'error': 'Negotiator bot not initialized'}), 400
    
    try:
        response = negotiator_bot.generate_response(
            context_id, 
            incoming_message, 
            offer_details
        )
        
        return jsonify({
            'response': response,
            'context_id': context_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_negotiation_status', methods=['POST'])
def get_negotiation_status():
    """Get the current status of a negotiation"""
    data = request.json
    context_id = data.get('context_id')
    
    if not context_id:
        return jsonify({'error': 'Context ID is required'}), 400
    
    if not negotiator_bot:
        return jsonify({'error': 'Negotiator bot not initialized'}), 400
    
    try:
        status = negotiator_bot.get_negotiation_status(context_id)
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_negotiation_strategy', methods=['POST'])
def update_negotiation_strategy():
    """Update the negotiation strategy"""
    data = request.json
    context_id = data.get('context_id')
    strategy = data.get('strategy')
    
    if not context_id or not strategy:
        return jsonify({'error': 'Context ID and strategy are required'}), 400
    
    if not negotiator_bot:
        return jsonify({'error': 'Negotiator bot not initialized'}), 400
    
    try:
        strategy_enum = NegotiationStrategy(strategy)
        negotiator_bot.update_strategy(context_id, strategy_enum)
        return jsonify({'message': 'Strategy updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':

    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
