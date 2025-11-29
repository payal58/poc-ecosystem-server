"""
Script to restore events to the database
Run: python restore_events.py
"""
from app.database import SessionLocal
from app.models import Event
from datetime import date, timedelta

db = SessionLocal()

try:
    # Check if events already exist
    existing_count = db.query(Event).count()
    if existing_count > 0:
        print(f"⚠️  {existing_count} events already exist. Skipping restoration.")
        print("   If you want to restore events anyway, delete them first.")
    else:
        # Seed Events (25 events)
        today = date.today()
        events = [
            Event(
                title="Tech Innovation Summit 2025",
                description="Join us for a day of innovation, networking, and cutting-edge technology demonstrations. Featuring keynote speakers from leading tech companies.",
                category="Conference",
                audience="Entrepreneurs, Students, Tech Professionals",
                location="Windsor Convention Centre",
                start_date=today + timedelta(days=30),
                end_date=today + timedelta(days=30),
                link="https://example.com/tech-summit"
            ),
            Event(
                title="Startup Pitch Night",
                description="Local startups pitch their ideas to investors and mentors. Open mic format with networking reception.",
                category="Networking",
                audience="Entrepreneurs, Investors",
                location="Innovation Hub",
                start_date=today + timedelta(days=15),
                link="https://example.com/pitch-night"
            ),
            Event(
                title="Women in Tech Workshop",
                description="Empowering women in technology through workshops and mentorship. Panel discussion with successful female tech leaders.",
                category="Workshop",
                audience="Women in Tech, Students",
                location="University of Windsor",
                start_date=today + timedelta(days=20),
                link="https://example.com/women-tech"
            ),
            Event(
                title="AI & Machine Learning Bootcamp",
                description="Intensive 3-day bootcamp covering AI fundamentals, machine learning applications, and hands-on projects.",
                category="Workshop",
                audience="Developers, Data Scientists, Entrepreneurs",
                location="TechStart Windsor",
                start_date=today + timedelta(days=45),
                end_date=today + timedelta(days=47),
                link="https://example.com/ai-bootcamp"
            ),
            Event(
                title="Entrepreneur Networking Mixer",
                description="Monthly networking event for entrepreneurs to connect, share ideas, and build relationships.",
                category="Networking",
                audience="Entrepreneurs, Business Owners",
                location="Windsor Co-working Collective",
                start_date=today + timedelta(days=10),
                link="https://example.com/networking-mixer"
            ),
            Event(
                title="Funding Opportunities Workshop",
                description="Learn about various funding options available for startups including grants, loans, and equity financing.",
                category="Workshop",
                audience="Entrepreneurs, Startup Founders",
                location="Windsor Business Development Centre",
                start_date=today + timedelta(days=25),
                link="https://example.com/funding-workshop"
            ),
            Event(
                title="GreenTech Innovation Day",
                description="Showcase of green technology innovations with presentations from sustainable startups and panel discussions.",
                category="Conference",
                audience="GreenTech Entrepreneurs, Environmentalists",
                location="GreenTech Ventures Office",
                start_date=today + timedelta(days=60),
                link="https://example.com/greentech-day"
            ),
            Event(
                title="Digital Marketing Masterclass",
                description="Learn effective digital marketing strategies for startups including social media, SEO, and content marketing.",
                category="Workshop",
                audience="Entrepreneurs, Marketing Professionals",
                location="Windsor Digital Media Lab",
                start_date=today + timedelta(days=35),
                link="https://example.com/digital-marketing"
            ),
            Event(
                title="Student Startup Showcase",
                description="University students present their startup ideas to judges and potential investors.",
                category="Competition",
                audience="Students, Educators, Investors",
                location="University of Windsor",
                start_date=today + timedelta(days=50),
                link="https://example.com/student-showcase"
            ),
            Event(
                title="Manufacturing Innovation Forum",
                description="Forum discussing the future of manufacturing, Industry 4.0, and smart manufacturing technologies.",
                category="Conference",
                audience="Manufacturing Professionals, Tech Entrepreneurs",
                location="Windsor Manufacturing Innovation Hub",
                start_date=today + timedelta(days=40),
                link="https://example.com/manufacturing-forum"
            ),
            Event(
                title="HealthTech Hackathon",
                description="48-hour hackathon focused on developing solutions for healthcare challenges. Prizes for top teams.",
                category="Competition",
                audience="Developers, Healthcare Professionals, Students",
                location="Windsor HealthTech Accelerator",
                start_date=today + timedelta(days=55),
                end_date=today + timedelta(days=57),
                link="https://example.com/healthtech-hackathon"
            ),
            Event(
                title="Women Entrepreneurs Power Lunch",
                description="Monthly lunch meeting for women entrepreneurs to network, share experiences, and support each other.",
                category="Networking",
                audience="Women Entrepreneurs",
                location="Downtown Restaurant",
                start_date=today + timedelta(days=12),
                link="https://example.com/women-power-lunch"
            ),
            Event(
                title="Business Model Canvas Workshop",
                description="Learn how to create and validate your business model using the Business Model Canvas framework.",
                category="Workshop",
                audience="Entrepreneurs, Startup Founders",
                location="Windsor Startup Foundry",
                start_date=today + timedelta(days=18),
                link="https://example.com/business-model"
            ),
            Event(
                title="Export Readiness Program",
                description="Multi-week program helping businesses prepare for international expansion with market research and export strategies.",
                category="Training",
                audience="Business Owners, Export-ready Companies",
                location="Windsor Export Development Office",
                start_date=today + timedelta(days=70),
                end_date=today + timedelta(days=84),
                link="https://example.com/export-program"
            ),
            Event(
                title="Food Innovation Demo Day",
                description="Food and beverage startups showcase their products and innovations to potential customers and investors.",
                category="Showcase",
                audience="Food Entrepreneurs, Investors, Foodies",
                location="Windsor Food Innovation Centre",
                start_date=today + timedelta(days=38),
                link="https://example.com/food-demo-day"
            ),
            Event(
                title="Youth Entrepreneurship Bootcamp",
                description="Week-long bootcamp for young entrepreneurs aged 16-30 covering ideation, validation, and launch strategies.",
                category="Training",
                audience="Youth Entrepreneurs (16-30), Students",
                location="Windsor Youth Entrepreneurship Program",
                start_date=today + timedelta(days=65),
                end_date=today + timedelta(days=71),
                link="https://example.com/youth-bootcamp"
            ),
            Event(
                title="Angel Investor Meetup",
                description="Private event connecting startup founders with angel investors for pitch sessions and networking.",
                category="Networking",
                audience="Startup Founders, Angel Investors",
                location="Windsor Angel Network",
                start_date=today + timedelta(days=22),
                link="https://example.com/angel-meetup"
            ),
            Event(
                title="TechBridge Career Fair",
                description="Career fair connecting tech professionals with local tech companies and startups.",
                category="Career",
                audience="Tech Professionals, Students, Job Seekers",
                location="TechBridge Windsor",
                start_date=today + timedelta(days=42),
                link="https://example.com/tech-career-fair"
            ),
            Event(
                title="Legal Essentials for Startups",
                description="Workshop covering essential legal topics for startups including incorporation, IP protection, and contracts.",
                category="Workshop",
                audience="Startup Founders, Entrepreneurs",
                location="Windsor Business Development Centre",
                start_date=today + timedelta(days=28),
                link="https://example.com/legal-essentials"
            ),
            Event(
                title="Innovation Ecosystem Summit",
                description="Annual summit bringing together all stakeholders in the Windsor-Essex innovation ecosystem.",
                category="Conference",
                audience="All ecosystem participants",
                location="Windsor Convention Centre",
                start_date=today + timedelta(days=90),
                end_date=today + timedelta(days=91),
                link="https://example.com/ecosystem-summit"
            ),
            Event(
                title="Startup Founder Circle",
                description="Exclusive monthly meeting for startup founders to share challenges, solutions, and support each other.",
                category="Networking",
                audience="Startup Founders, Co-founders",
                location="Windsor Startup Foundry",
                start_date=today + timedelta(days=8),
                link="https://example.com/founder-circle"
            ),
            Event(
                title="Product-Market Fit Workshop",
                description="Learn how to validate product-market fit through customer discovery and iterative testing.",
                category="Workshop",
                audience="Product Managers, Entrepreneurs",
                location="TechStart Windsor",
                start_date=today + timedelta(days=32),
                link="https://example.com/product-market-fit"
            ),
            Event(
                title="FinTech Innovation Panel",
                description="Panel discussion on financial technology innovations, trends, and opportunities in the fintech space.",
                category="Conference",
                audience="FinTech Entrepreneurs, Financial Professionals",
                location="Windsor Innovation Hub",
                start_date=today + timedelta(days=48),
                link="https://example.com/fintech-panel"
            ),
            Event(
                title="Co-working Open House",
                description="Open house event showcasing co-working facilities and welcoming new members to the community.",
                category="Networking",
                audience="Freelancers, Remote Workers, Entrepreneurs",
                location="Windsor Co-working Collective",
                start_date=today + timedelta(days=5),
                link="https://example.com/coworking-openhouse"
            ),
            Event(
                title="Mentorship Matchmaking Event",
                description="Connect experienced mentors with entrepreneurs seeking guidance in a speed-mentoring format.",
                category="Networking",
                audience="Entrepreneurs, Mentors, Mentees",
                location="Windsor-Essex Innovation Hub",
                start_date=today + timedelta(days=33),
                link="https://example.com/mentorship-matchmaking"
            ),
        ]
        
        for event in events:
            db.add(event)
        
        db.commit()
        print(f"✅ Successfully restored {len(events)} events to the database!")
        
except Exception as e:
    print(f"❌ Error restoring events: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()

