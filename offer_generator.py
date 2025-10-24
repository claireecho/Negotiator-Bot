"""
Offer Generator for Negotiator Bot vs Recruiter Bot
Provides diverse job offers from various companies
"""

import random
from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum

class CompanyType(Enum):
    TECH_GIANT = "tech_giant"
    STARTUP = "startup"
    FINANCE = "finance"
    CONSULTING = "consulting"
    HEALTHCARE = "healthcare"
    AUTOMOTIVE = "automotive"
    RETAIL = "retail"
    MEDIA = "media"

@dataclass
class JobOffer:
    company_name: str
    position: str
    base_salary: int
    company_type: CompanyType
    industry: str
    benefits: List[str]
    location: str
    company_size: str
    description: str
    negotiation_difficulty: float  # 0.0 (easy) to 1.0 (hard)

class OfferGenerator:
    def __init__(self):
        self.companies = {
            CompanyType.TECH_GIANT: [
                {"name": "Google", "size": "Large", "location": "Mountain View, CA"},
                {"name": "Microsoft", "size": "Large", "location": "Redmond, WA"},
                {"name": "Apple", "size": "Large", "location": "Cupertino, CA"},
                {"name": "Amazon", "size": "Large", "location": "Seattle, WA"},
                {"name": "Meta", "size": "Large", "location": "Menlo Park, CA"},
                {"name": "Netflix", "size": "Large", "location": "Los Gatos, CA"},
                {"name": "Tesla", "size": "Large", "location": "Austin, TX"},
                {"name": "NVIDIA", "size": "Large", "location": "Santa Clara, CA"},
            ],
            CompanyType.STARTUP: [
                {"name": "OpenAI", "size": "Medium", "location": "San Francisco, CA"},
                {"name": "Anthropic", "size": "Medium", "location": "San Francisco, CA"},
                {"name": "Stripe", "size": "Medium", "location": "San Francisco, CA"},
                {"name": "Airbnb", "size": "Medium", "location": "San Francisco, CA"},
                {"name": "Uber", "size": "Medium", "location": "San Francisco, CA"},
                {"name": "Lyft", "size": "Medium", "location": "San Francisco, CA"},
                {"name": "Pinterest", "size": "Medium", "location": "San Francisco, CA"},
                {"name": "Slack", "size": "Medium", "location": "San Francisco, CA"},
            ],
            CompanyType.FINANCE: [
                {"name": "Goldman Sachs", "size": "Large", "location": "New York, NY"},
                {"name": "JPMorgan Chase", "size": "Large", "location": "New York, NY"},
                {"name": "Morgan Stanley", "size": "Large", "location": "New York, NY"},
                {"name": "BlackRock", "size": "Large", "location": "New York, NY"},
                {"name": "Visa", "size": "Large", "location": "Foster City, CA"},
                {"name": "PayPal", "size": "Large", "location": "San Jose, CA"},
                {"name": "Square", "size": "Medium", "location": "San Francisco, CA"},
                {"name": "Robinhood", "size": "Medium", "location": "Menlo Park, CA"},
            ],
            CompanyType.CONSULTING: [
                {"name": "McKinsey & Company", "size": "Large", "location": "New York, NY"},
                {"name": "Boston Consulting Group", "size": "Large", "location": "Boston, MA"},
                {"name": "Bain & Company", "size": "Large", "location": "Boston, MA"},
                {"name": "Deloitte", "size": "Large", "location": "New York, NY"},
                {"name": "PwC", "size": "Large", "location": "New York, NY"},
                {"name": "Accenture", "size": "Large", "location": "New York, NY"},
                {"name": "EY", "size": "Large", "location": "New York, NY"},
                {"name": "KPMG", "size": "Large", "location": "New York, NY"},
            ],
            CompanyType.HEALTHCARE: [
                {"name": "Johnson & Johnson", "size": "Large", "location": "New Brunswick, NJ"},
                {"name": "Pfizer", "size": "Large", "location": "New York, NY"},
                {"name": "Merck", "size": "Large", "location": "Kenilworth, NJ"},
                {"name": "Abbott", "size": "Large", "location": "Abbott Park, IL"},
                {"name": "Medtronic", "size": "Large", "location": "Minneapolis, MN"},
                {"name": "UnitedHealth Group", "size": "Large", "location": "Minnetonka, MN"},
                {"name": "Anthem", "size": "Large", "location": "Indianapolis, IN"},
                {"name": "Cigna", "size": "Large", "location": "Bloomfield, CT"},
            ],
            CompanyType.AUTOMOTIVE: [
                {"name": "Ford", "size": "Large", "location": "Dearborn, MI"},
                {"name": "General Motors", "size": "Large", "location": "Detroit, MI"},
                {"name": "BMW", "size": "Large", "location": "Munich, Germany"},
                {"name": "Mercedes-Benz", "size": "Large", "location": "Stuttgart, Germany"},
                {"name": "Toyota", "size": "Large", "location": "Toyota City, Japan"},
                {"name": "Honda", "size": "Large", "location": "Tokyo, Japan"},
                {"name": "Volkswagen", "size": "Large", "location": "Wolfsburg, Germany"},
                {"name": "Hyundai", "size": "Large", "location": "Seoul, South Korea"},
            ],
            CompanyType.RETAIL: [
                {"name": "Walmart", "size": "Large", "location": "Bentonville, AR"},
                {"name": "Amazon", "size": "Large", "location": "Seattle, WA"},
                {"name": "Target", "size": "Large", "location": "Minneapolis, MN"},
                {"name": "Costco", "size": "Large", "location": "Issaquah, WA"},
                {"name": "Home Depot", "size": "Large", "location": "Atlanta, GA"},
                {"name": "Lowe's", "size": "Large", "location": "Mooresville, NC"},
                {"name": "Best Buy", "size": "Large", "location": "Richfield, MN"},
                {"name": "Macy's", "size": "Large", "location": "New York, NY"},
            ],
            CompanyType.MEDIA: [
                {"name": "Disney", "size": "Large", "location": "Burbank, CA"},
                {"name": "Netflix", "size": "Large", "location": "Los Gatos, CA"},
                {"name": "Warner Bros", "size": "Large", "location": "Burbank, CA"},
                {"name": "Sony Pictures", "size": "Large", "location": "Culver City, CA"},
                {"name": "Paramount", "size": "Large", "location": "Hollywood, CA"},
                {"name": "Universal", "size": "Large", "location": "Universal City, CA"},
                {"name": "HBO", "size": "Large", "location": "New York, NY"},
                {"name": "Hulu", "size": "Medium", "location": "Santa Monica, CA"},
            ]
        }
        
        self.positions = {
            "Software Engineer": {
                "levels": ["I", "II", "Senior", "Staff", "Principal"],
                "base_salary_range": (80000, 200000),
                "benefits": ["health_insurance", "401k", "stock_options", "unlimited_pto", "remote_work"]
            },
            "Data Scientist": {
                "levels": ["I", "II", "Senior", "Staff", "Principal"],
                "base_salary_range": (90000, 220000),
                "benefits": ["health_insurance", "401k", "stock_options", "unlimited_pto", "remote_work", "conference_budget"]
            },
            "Product Manager": {
                "levels": ["Associate", "I", "II", "Senior", "Principal"],
                "base_salary_range": (100000, 250000),
                "benefits": ["health_insurance", "401k", "stock_options", "unlimited_pto", "remote_work", "bonus"]
            },
            "UX Designer": {
                "levels": ["I", "II", "Senior", "Staff", "Principal"],
                "base_salary_range": (75000, 180000),
                "benefits": ["health_insurance", "401k", "stock_options", "unlimited_pto", "remote_work", "design_budget"]
            },
            "DevOps Engineer": {
                "levels": ["I", "II", "Senior", "Staff", "Principal"],
                "base_salary_range": (85000, 190000),
                "benefits": ["health_insurance", "401k", "stock_options", "unlimited_pto", "remote_work", "on_call_bonus"]
            },
            "Machine Learning Engineer": {
                "levels": ["I", "II", "Senior", "Staff", "Principal"],
                "base_salary_range": (95000, 230000),
                "benefits": ["health_insurance", "401k", "stock_options", "unlimited_pto", "remote_work", "research_budget"]
            },
            "Sales Engineer": {
                "levels": ["I", "II", "Senior", "Staff", "Principal"],
                "base_salary_range": (80000, 200000),
                "benefits": ["health_insurance", "401k", "commission", "unlimited_pto", "remote_work", "travel_budget"]
            },
            "Marketing Manager": {
                "levels": ["I", "II", "Senior", "Staff", "Principal"],
                "base_salary_range": (70000, 160000),
                "benefits": ["health_insurance", "401k", "bonus", "unlimited_pto", "remote_work", "marketing_budget"]
            }
        }
        
        self.benefit_descriptions = {
            "health_insurance": "Comprehensive health, dental, and vision insurance",
            "401k": "401(k) with company matching up to 6%",
            "stock_options": "Equity participation and stock options",
            "unlimited_pto": "Unlimited paid time off",
            "remote_work": "Flexible remote work options",
            "conference_budget": "Annual conference and training budget",
            "bonus": "Performance-based annual bonus",
            "design_budget": "Annual design tools and software budget",
            "on_call_bonus": "On-call and overtime compensation",
            "research_budget": "Research and development budget",
            "commission": "Sales commission structure",
            "travel_budget": "Business travel and entertainment budget",
            "marketing_budget": "Marketing campaign and tools budget"
        }

    def generate_offer(self, company_type: CompanyType = None) -> JobOffer:
        """Generate a random job offer"""
        if company_type is None:
            company_type = random.choice(list(CompanyType))
        
        # Select company
        company_info = random.choice(self.companies[company_type])
        
        # Select position
        position_name = random.choice(list(self.positions.keys()))
        position_info = self.positions[position_name]
        level = random.choice(position_info["levels"])
        full_position = f"{position_name} {level}"
        
        # Generate salary based on company type and position
        base_range = position_info["base_salary_range"]
        company_multiplier = self._get_company_multiplier(company_type, company_info["name"])
        base_salary = int(random.uniform(*base_range) * company_multiplier)
        
        # Select benefits
        available_benefits = position_info["benefits"].copy()
        if company_type == CompanyType.TECH_GIANT:
            available_benefits.extend(["free_meals", "gym_membership", "transportation"])
        elif company_type == CompanyType.STARTUP:
            available_benefits.extend(["equity", "flexible_hours", "startup_perks"])
        elif company_type == CompanyType.FINANCE:
            available_benefits.extend(["bonus", "retirement_plan", "financial_planning"])
        
        selected_benefits = random.sample(available_benefits, min(4, len(available_benefits)))
        
        # Generate description
        description = self._generate_description(company_info["name"], full_position, company_type)
        
        # Calculate negotiation difficulty
        negotiation_difficulty = self._calculate_negotiation_difficulty(company_type, company_info["size"])
        
        return JobOffer(
            company_name=company_info["name"],
            position=full_position,
            base_salary=base_salary,
            company_type=company_type,
            industry=company_type.value,
            benefits=selected_benefits,
            location=company_info["location"],
            company_size=company_info["size"],
            description=description,
            negotiation_difficulty=negotiation_difficulty
        )

    def _get_company_multiplier(self, company_type: CompanyType, company_name: str) -> float:
        """Get salary multiplier based on company type and name"""
        multipliers = {
            CompanyType.TECH_GIANT: 1.2,
            CompanyType.STARTUP: 1.0,
            CompanyType.FINANCE: 1.3,
            CompanyType.CONSULTING: 1.1,
            CompanyType.HEALTHCARE: 0.9,
            CompanyType.AUTOMOTIVE: 0.95,
            CompanyType.RETAIL: 0.85,
            CompanyType.MEDIA: 1.05
        }
        
        # Special cases for high-paying companies
        high_paying = ["Google", "Microsoft", "Apple", "Amazon", "Meta", "Netflix", "Tesla", "NVIDIA", "OpenAI", "Anthropic"]
        if company_name in high_paying:
            return multipliers[company_type] * 1.1
        
        return multipliers[company_type]

    def _generate_description(self, company_name: str, position: str, company_type: CompanyType) -> str:
        """Generate a job offer description"""
        descriptions = {
            CompanyType.TECH_GIANT: f"Join {company_name}, a leading technology company, as a {position}. You'll work on cutting-edge projects that impact millions of users worldwide.",
            CompanyType.STARTUP: f"Be part of {company_name}'s innovative team as a {position}. Help shape the future of technology in a fast-paced, collaborative environment.",
            CompanyType.FINANCE: f"Join {company_name} as a {position} and work on financial solutions that power global markets. Competitive compensation and excellent benefits.",
            CompanyType.CONSULTING: f"Work with {company_name} as a {position} to solve complex business challenges for Fortune 500 clients worldwide.",
            CompanyType.HEALTHCARE: f"Make a difference at {company_name} as a {position}, contributing to healthcare innovation and improving patient outcomes.",
            CompanyType.AUTOMOTIVE: f"Drive innovation at {company_name} as a {position}, working on the future of transportation and mobility solutions.",
            CompanyType.RETAIL: f"Join {company_name} as a {position} and help shape the future of retail and e-commerce experiences.",
            CompanyType.MEDIA: f"Create compelling content and experiences at {company_name} as a {position} in the entertainment industry."
        }
        
        return descriptions[company_type]

    def _calculate_negotiation_difficulty(self, company_type: CompanyType, company_size: str) -> float:
        """Calculate how difficult it will be to negotiate with this company"""
        base_difficulty = {
            CompanyType.TECH_GIANT: 0.3,  # Easy to negotiate
            CompanyType.STARTUP: 0.2,     # Very easy
            CompanyType.FINANCE: 0.7,     # Hard
            CompanyType.CONSULTING: 0.6,  # Medium-hard
            CompanyType.HEALTHCARE: 0.8,  # Very hard
            CompanyType.AUTOMOTIVE: 0.5,  # Medium
            CompanyType.RETAIL: 0.9,      # Very hard
            CompanyType.MEDIA: 0.4        # Easy-medium
        }
        
        size_multiplier = 0.8 if company_size == "Large" else 1.0
        return min(1.0, base_difficulty[company_type] * size_multiplier)

    def get_offer_summary(self, offer: JobOffer) -> str:
        """Get a formatted summary of the job offer"""
        benefits_text = ", ".join([self.benefit_descriptions.get(b, b) for b in offer.benefits])
        
        return f"""
🏢 **{offer.company_name}** - {offer.position}
💰 **Salary**: ${offer.base_salary:,}
📍 **Location**: {offer.location}
🏢 **Company Size**: {offer.company_size}
📋 **Description**: {offer.description}

**Benefits:**
{benefits_text}

**Negotiation Difficulty**: {'Easy' if offer.negotiation_difficulty < 0.4 else 'Medium' if offer.negotiation_difficulty < 0.7 else 'Hard'}
        """.strip()

    def generate_multiple_offers(self, count: int = 5) -> List[JobOffer]:
        """Generate multiple diverse job offers"""
        offers = []
        used_companies = set()
        
        for _ in range(count):
            # Try to get diverse company types
            company_types = list(CompanyType)
            random.shuffle(company_types)
            
            for company_type in company_types:
                offer = self.generate_offer(company_type)
                if offer.company_name not in used_companies:
                    offers.append(offer)
                    used_companies.add(offer.company_name)
                    break
            else:
                # If all companies used, generate any offer
                offers.append(self.generate_offer())
        
        return offers[:count]

# Example usage
if __name__ == "__main__":
    generator = OfferGenerator()
    
    print("🎯 Sample Job Offers:")
    print("=" * 50)
    
    offers = generator.generate_multiple_offers(3)
    for i, offer in enumerate(offers, 1):
        print(f"\n{i}. {generator.get_offer_summary(offer)}")
        print("-" * 50)
