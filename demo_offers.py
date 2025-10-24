#!/usr/bin/env python3
"""
Demo script to showcase the variety of job offers
"""

import requests
import json
from offer_generator import OfferGenerator, CompanyType

def demo_offer_generator():
    """Demo the offer generator directly"""
    print("🎯 Direct Offer Generator Demo")
    print("=" * 60)
    
    generator = OfferGenerator()
    
    # Generate offers for each company type
    for company_type in CompanyType:
        print(f"\n🏢 {company_type.value.upper().replace('_', ' ')} COMPANIES:")
        print("-" * 40)
        
        offers = generator.generate_multiple_offers(2)
        for i, offer in enumerate(offers, 1):
            print(f"{i}. {offer.company_name} - {offer.position}")
            print(f"   💰 ${offer.base_salary:,} | 📍 {offer.location}")
            print(f"   📊 Difficulty: {'Easy' if offer.negotiation_difficulty < 0.4 else 'Medium' if offer.negotiation_difficulty < 0.7 else 'Hard'}")
            print()

def demo_api_endpoints():
    """Demo the API endpoints"""
    print("🌐 API Endpoints Demo")
    print("=" * 60)
    
    base_url = "http://localhost:8080"
    
    try:
        # Test health endpoint
        print("1. Health Check:")
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.json()}")
        print()
        
        # Test random offer endpoint
        print("2. Random Offer:")
        response = requests.get(f"{base_url}/get_random_offer")
        offer = response.json()
        print(f"   Company: {offer['company_name']}")
        print(f"   Position: {offer['position']}")
        print(f"   Salary: ${offer['base_salary']:,}")
        print(f"   Location: {offer['location']}")
        print()
        
        # Test multiple offers endpoint
        print("3. Multiple Offers (5 companies):")
        response = requests.get(f"{base_url}/get_multiple_offers?count=5")
        offers = response.json()
        
        for i, offer in enumerate(offers, 1):
            print(f"   {i}. {offer['company_name']} - {offer['position']} (${offer['base_salary']:,})")
        print()
        
        # Test company type filtering
        print("4. Tech Giant Offers:")
        response = requests.get(f"{base_url}/get_random_offer?company_type=tech_giant")
        offer = response.json()
        print(f"   Company: {offer['company_name']}")
        print(f"   Position: {offer['position']}")
        print(f"   Salary: ${offer['base_salary']:,}")
        print()
        
        print("5. Startup Offers:")
        response = requests.get(f"{base_url}/get_random_offer?company_type=startup")
        offer = response.json()
        print(f"   Company: {offer['company_name']}")
        print(f"   Position: {offer['position']}")
        print(f"   Salary: ${offer['base_salary']:,}")
        print()
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask server. Make sure it's running on port 8080")
        print("   Run: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_company_variety():
    """Demo the variety of companies available"""
    print("🏢 Company Variety Demo")
    print("=" * 60)
    
    generator = OfferGenerator()
    
    # Show all available companies
    for company_type, companies in generator.companies.items():
        print(f"\n{company_type.value.upper().replace('_', ' ')}:")
        for company in companies[:4]:  # Show first 4 companies
            print(f"  • {company['name']} ({company['location']})")
        if len(companies) > 4:
            print(f"  ... and {len(companies) - 4} more")
    
    print(f"\n📊 Total Companies: {sum(len(companies) for companies in generator.companies.values())}")
    print(f"📊 Company Types: {len(generator.companies)}")
    print(f"📊 Positions: {len(generator.positions)}")

def demo_salary_ranges():
    """Demo salary ranges by company type"""
    print("💰 Salary Range Demo")
    print("=" * 60)
    
    generator = OfferGenerator()
    
    for company_type in CompanyType:
        offers = [generator.generate_offer(company_type) for _ in range(5)]
        salaries = [offer.base_salary for offer in offers]
        
        print(f"{company_type.value.upper().replace('_', ' ')}:")
        print(f"  Range: ${min(salaries):,} - ${max(salaries):,}")
        print(f"  Average: ${sum(salaries) // len(salaries):,}")
        print()

def main():
    """Main demo function"""
    print("🤖 Negotiator Bot vs Recruiter Bot - Offer Variety Demo")
    print("=" * 80)
    
    # Demo 1: Direct offer generator
    demo_offer_generator()
    
    print("\n" + "=" * 80)
    
    # Demo 2: API endpoints
    demo_api_endpoints()
    
    print("\n" + "=" * 80)
    
    # Demo 3: Company variety
    demo_company_variety()
    
    print("\n" + "=" * 80)
    
    # Demo 4: Salary ranges
    demo_salary_ranges()
    
    print("\n🎉 Demo completed!")
    print("\nTo use the full application:")
    print("  • Flask version: python main.py")
    print("  • Streamlit version: streamlit run streamlit_app.py")

if __name__ == "__main__":
    main()
