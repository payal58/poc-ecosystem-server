"""
Seed script to populate database with demo data
Run this after migrations: python seed_data.py
"""
from app.database import SessionLocal, engine, Base
from app.models import Event, Organization, Pathway, SearchLog, Program
from datetime import date, datetime, timedelta
import random

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Clear existing data (optional - comment out if you want to keep existing data)
    db.query(SearchLog).delete()
    db.query(Pathway).delete()
    db.query(Program).delete()
    db.query(Event).delete()
    db.query(Organization).delete()
    db.commit()
    
    # Seed Organizations (20 organizations with new structure)
    organizations = [
        Organization(
            business_name="Windsor-Essex Innovation Hub",
            business_stage="Established Business",
            description="Leading innovation center supporting startups and entrepreneurs in the region with state-of-the-art facilities and expert mentorship.",
            industry="Technology",
            business_sector="Innovation & Technology",
            business_location="Windsor, Ontario",
            legal_structure="Non-Profit",
            business_status="Active",
            website="https://example.com/innovation-hub",
            email="info@innovationhub.com",
            phone_number="(519) 555-0100",
            social_media={
                "LinkedIn": "https://linkedin.com/company/innovation-hub",
                "Twitter/X": "https://twitter.com/innovationhub",
                "Facebook": "https://facebook.com/innovationhub"
            },
            additional_contact_info="Contact us for startup support and mentorship programs."
        ),
        Organization(
            business_name="TechStart Windsor",
            business_stage="Established Business",
            description="Accelerator program for tech startups with mentorship and funding opportunities. We help startups scale from idea to market.",
            industry="Technology",
            business_sector="Accelerator",
            business_location="Windsor, Ontario",
            legal_structure="LLC",
            business_status="Active",
            website="https://example.com/techstart",
            email="contact@techstart.com",
            phone_number="(519) 555-0101",
            social_media={
                "LinkedIn": "https://linkedin.com/company/techstart",
                "Twitter/X": "https://twitter.com/techstart"
            }
        ),
        Organization(
            business_name="Entrepreneur Network Windsor",
            business_stage="Growing Business",
            description="Community of entrepreneurs sharing knowledge and resources. Monthly meetups and networking events.",
            industry="Business Services",
            business_sector="Network",
            business_location="Windsor, Ontario",
            legal_structure="Non-Profit",
            business_status="Active",
            website="https://example.com/entrepreneur-network",
            email="hello@entnetwork.com",
            phone_number="(519) 555-0102",
            social_media={
                "LinkedIn": "https://linkedin.com/company/entnetwork",
                "Facebook": "https://facebook.com/entnetwork"
            }
        ),
        Organization(
            business_name="University of Windsor - Innovation Centre",
            business_stage="Established Business",
            description="University-based innovation center supporting student and faculty entrepreneurship with research facilities.",
            industry="Education",
            business_sector="University",
            business_location="Windsor, Ontario",
            legal_structure="Non-Profit",
            business_status="Active",
            website="https://example.com/uwindsor-innovation",
            email="innovation@uwindsor.ca",
            phone_number="(519) 555-0103"
        ),
        Organization(
            business_name="St. Clair College - Entrepreneurship Program",
            business_stage="Established Business",
            description="Comprehensive entrepreneurship program offering courses, mentorship, and startup support for students and community members.",
            industry="Education",
            business_sector="College",
            business_location="Windsor, Ontario",
            legal_structure="Non-Profit",
            business_status="Active",
            website="https://example.com/stclair-entrepreneurship",
            email="entrepreneurship@stclaircollege.ca",
            phone_number="(519) 555-0104"
        ),
        Organization(
            business_name="Windsor-Essex Economic Development Corporation",
            business_stage="Established Business",
            description="Supporting local businesses with economic development initiatives, funding programs, and business advisory services.",
            industry="Government",
            business_sector="Economic Development",
            business_location="Windsor, Ontario",
            legal_structure="Corporation",
            business_status="Active",
            website="https://example.com/we-edc",
            email="info@we-edc.ca",
            phone_number="(519) 555-0105"
        ),
        Organization(
            business_name="GreenTech Ventures",
            business_stage="Established Business",
            description="Venture capital firm specializing in green technology and sustainable innovation startups.",
            industry="Finance",
            business_sector="Venture Capital",
            business_location="Windsor, Ontario",
            legal_structure="Corporation",
            business_status="Active",
            website="https://example.com/greentech-ventures",
            email="invest@greentechventures.com",
            phone_number="(519) 555-0106",
            social_media={
                "LinkedIn": "https://linkedin.com/company/greentech",
                "Twitter/X": "https://twitter.com/greentech"
            }
        ),
        Organization(
            business_name="Windsor Startup Foundry",
            business_stage="Growing Business",
            description="Early-stage startup incubator providing workspace, mentorship, and access to investor network.",
            industry="Technology",
            business_sector="Incubator",
            business_location="Windsor, Ontario",
            legal_structure="LLC",
            business_status="Active",
            website="https://example.com/startup-foundry",
            email="info@startupfoundry.ca",
            phone_number="(519) 555-0107"
        ),
        Organization(
            business_name="Windsor Business Development Centre",
            business_stage="Established Business",
            description="Comprehensive business development services including market research, business planning, and growth strategies.",
            industry="Business Services",
            business_sector="Consulting",
            business_location="Windsor, Ontario",
            legal_structure="Corporation",
            business_status="Active",
            website="https://example.com/business-dev",
            email="info@bizdevcentre.ca",
            phone_number="(519) 555-0108"
        ),
        Organization(
            business_name="TechBridge Windsor",
            business_stage="Growing Business",
            description="Connecting tech talent with opportunities through workshops, networking, and career development programs.",
            industry="Technology",
            business_sector="Network",
            business_location="Windsor, Ontario",
            legal_structure="Non-Profit",
            business_status="Active",
            website="https://example.com/techbridge",
            email="hello@techbridge.ca",
            phone_number="(519) 555-0109",
            social_media={
                "LinkedIn": "https://linkedin.com/company/techbridge",
                "Twitter/X": "https://twitter.com/techbridge"
            }
        ),
        Organization(
            business_name="Windsor Angel Network",
            business_stage="Established Business",
            description="Angel investor network connecting entrepreneurs with experienced investors and mentors.",
            industry="Finance",
            business_sector="Investment",
            business_location="Windsor, Ontario",
            legal_structure="Partnership",
            business_status="Active",
            website="https://example.com/angel-network",
            email="info@angelnetwork.ca",
            phone_number="(519) 555-0110"
        ),
        Organization(
            business_name="Women Entrepreneurs Windsor",
            business_stage="Growing Business",
            description="Supporting women entrepreneurs through mentorship, networking, and business development programs.",
            industry="Business Services",
            business_sector="Network",
            business_location="Windsor, Ontario",
            legal_structure="Non-Profit",
            business_status="Active",
            website="https://example.com/women-entrepreneurs",
            email="contact@womenentrepreneurs.ca",
            phone_number="(519) 555-0111",
            social_media={
                "LinkedIn": "https://linkedin.com/company/women-entrepreneurs",
                "Facebook": "https://facebook.com/womenentrepreneurs",
                "Instagram": "https://instagram.com/womenentrepreneurs"
            }
        ),
        Organization(
            business_name="Windsor Manufacturing Innovation Hub",
            business_stage="Established Business",
            description="Supporting manufacturing startups with specialized equipment, expertise, and industry connections.",
            industry="Manufacturing",
            business_sector="Manufacturing",
            business_location="Windsor, Ontario",
            legal_structure="Corporation",
            business_status="Active",
            website="https://example.com/manufacturing-hub",
            email="info@manufacturinghub.ca",
            phone_number="(519) 555-0112"
        ),
        Organization(
            business_name="Windsor Digital Media Lab",
            business_stage="Early Stage",
            description="Co-working space and incubator for digital media, creative tech, and content creation startups.",
            industry="Media",
            business_sector="Creative",
            business_location="Windsor, Ontario",
            legal_structure="LLC",
            business_status="Active",
            website="https://example.com/digital-media-lab",
            email="info@digitalmedialab.ca",
            phone_number="(519) 555-0113",
            social_media={
                "Instagram": "https://instagram.com/digitalmedialab",
                "YouTube": "https://youtube.com/digitalmedialab"
            }
        ),
        Organization(
            business_name="Windsor Food Innovation Centre",
            business_stage="Growing Business",
            description="Supporting food and beverage startups with commercial kitchen access, regulatory guidance, and market connections.",
            industry="Food & Beverage",
            business_sector="Food & Beverage",
            business_location="Windsor, Ontario",
            legal_structure="LLC",
            business_status="Active",
            website="https://example.com/food-innovation",
            email="info@foodinnovation.ca",
            phone_number="(519) 555-0114"
        ),
        Organization(
            business_name="Windsor HealthTech Accelerator",
            business_stage="Established Business",
            description="Specialized accelerator for health technology startups with clinical partnerships and regulatory support.",
            industry="Healthcare",
            business_sector="Healthcare",
            business_location="Windsor, Ontario",
            legal_structure="Corporation",
            business_status="Active",
            website="https://example.com/healthtech-accelerator",
            email="info@healthtech.ca",
            phone_number="(519) 555-0115"
        ),
        Organization(
            business_name="Windsor Youth Entrepreneurship Program",
            business_stage="Growing Business",
            description="Empowering young entrepreneurs aged 16-30 with mentorship, workshops, and startup funding opportunities.",
            industry="Education",
            business_sector="Education",
            business_location="Windsor, Ontario",
            legal_structure="Non-Profit",
            business_status="Active",
            website="https://example.com/youth-entrepreneurship",
            email="youth@entrepreneurship.ca",
            phone_number="(519) 555-0116",
            social_media={
                "Instagram": "https://instagram.com/youthentrepreneurship",
                "TikTok": "https://tiktok.com/@youthentrepreneurship"
            }
        ),
        Organization(
            business_name="Windsor Export Development Office",
            business_stage="Established Business",
            description="Helping local businesses expand internationally through export programs, trade missions, and market intelligence.",
            industry="Business Services",
            business_sector="Export Services",
            business_location="Windsor, Ontario",
            legal_structure="Corporation",
            business_status="Active",
            website="https://example.com/export-office",
            email="export@windsor.ca",
            phone_number="(519) 555-0117"
        ),
        Organization(
            business_name="Windsor Co-working Collective",
            business_stage="Growing Business",
            description="Modern co-working space with flexible membership options, networking events, and business support services.",
            industry="Real Estate",
            business_sector="Co-working",
            business_location="Windsor, Ontario",
            legal_structure="LLC",
            business_status="Active",
            website="https://example.com/coworking",
            email="info@coworkingcollective.ca",
            phone_number="(519) 555-0118",
            social_media={
                "LinkedIn": "https://linkedin.com/company/coworkingcollective",
                "Instagram": "https://instagram.com/coworkingcollective"
            }
        ),
        Organization(
            business_name="Windsor Innovation Alliance",
            business_stage="Established Business",
            description="Non-profit organization connecting innovators, entrepreneurs, and investors to foster the local innovation ecosystem.",
            industry="Business Services",
            business_sector="Network",
            business_location="Windsor, Ontario",
            legal_structure="Non-Profit",
            business_status="Active",
            website="https://example.com/innovation-alliance",
            email="info@innovationalliance.ca",
            phone_number="(519) 555-0119",
            social_media={
                "LinkedIn": "https://linkedin.com/company/innovationalliance",
                "Twitter/X": "https://twitter.com/innovationalliance",
                "Facebook": "https://facebook.com/innovationalliance"
            }
        ),
    ]
    
    for org in organizations:
        db.add(org)
    
    db.commit()  # Commit organizations first to get IDs
    
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
    
    db.commit()  # Commit events to get IDs
    
    # Seed Pathways (5 pathways)
    pathways = [
        Pathway(
            question="What stage is your business in?",
            answer_options={
                "idea": "Idea",
                "early": "Early Stage",
                "growth": "Growing Business",
                "established": "Established Business"
            },
            recommended_resources={
                "idea": {
                    "organizations": [1, 4, 8],
                    "events": [1, 2, 13],
                    "description": "Consider joining our incubator program or attending networking events to validate your idea."
                },
                "early": {
                    "organizations": [1, 2, 8],
                    "events": [2, 13, 16],
                    "description": "Accelerator programs and pitch events would be beneficial for early-stage startups."
                },
                "growth": {
                    "organizations": [2, 3, 7],
                    "events": [1, 2, 6],
                    "description": "Focus on scaling and connecting with investors to fuel your growth."
                },
                "established": {
                    "organizations": [3, 18, 19],
                    "events": [14, 20],
                    "description": "Network with other established businesses and explore partnerships and export opportunities."
                }
            }
        ),
        Pathway(
            question="What type of support are you looking for?",
            answer_options={
                "funding": "Funding",
                "mentorship": "Mentorship",
                "networking": "Networking",
                "training": "Training/Education"
            },
            recommended_resources={
                "funding": {
                    "organizations": [2, 7, 11],
                    "events": [2, 17, 6],
                    "description": "Check out our accelerator program, angel investor network, and pitch events for funding opportunities."
                },
                "mentorship": {
                    "organizations": [1, 2, 8],
                    "events": [25, 21],
                    "description": "Incubators, accelerators, and mentorship programs offer structured mentorship opportunities."
                },
                "networking": {
                    "organizations": [3, 10, 20],
                    "events": [5, 12, 21, 24],
                    "description": "Join networking events and entrepreneur communities to build your professional network."
                },
                "training": {
                    "organizations": [4, 5, 17],
                    "events": [4, 13, 16],
                    "description": "University programs, workshops, and bootcamps provide comprehensive training opportunities."
                }
            }
        ),
        Pathway(
            question="What industry are you in or interested in?",
            answer_options={
                "tech": "Technology/Software",
                "health": "Healthcare/HealthTech",
                "green": "GreenTech/Sustainability",
                "food": "Food & Beverage",
                "manufacturing": "Manufacturing",
                "media": "Digital Media/Creative"
            },
            recommended_resources={
                "tech": {
                    "organizations": [2, 10, 8],
                    "events": [1, 4, 18],
                    "description": "Tech-focused accelerators and networking events are perfect for technology startups."
                },
                "health": {
                    "organizations": [16],
                    "events": [11],
                    "description": "HealthTech accelerator provides specialized support for healthcare technology startups."
                },
                "green": {
                    "organizations": [7],
                    "events": [7],
                    "description": "GreenTech Ventures specializes in sustainable innovation and green technology."
                },
                "food": {
                    "organizations": [15],
                    "events": [15],
                    "description": "Food Innovation Centre offers specialized support for food and beverage startups."
                },
                "manufacturing": {
                    "organizations": [13],
                    "events": [10],
                    "description": "Manufacturing Innovation Hub provides specialized equipment and industry expertise."
                },
                "media": {
                    "organizations": [14],
                    "events": [8],
                    "description": "Digital Media Lab supports creative tech and content creation startups."
                }
            }
        ),
        Pathway(
            question="What is your primary role?",
            answer_options={
                "founder": "Startup Founder/Entrepreneur",
                "student": "Student",
                "professional": "Working Professional",
                "investor": "Investor",
                "mentor": "Mentor/Advisor"
            },
            recommended_resources={
                "founder": {
                    "organizations": [1, 2, 8, 3],
                    "events": [2, 5, 21, 13],
                    "description": "As a founder, connect with incubators, accelerators, and networking events to grow your startup."
                },
                "student": {
                    "organizations": [4, 5, 17],
                    "events": [9, 16, 18],
                    "description": "Students can benefit from university programs, youth entrepreneurship programs, and student-focused events."
                },
                "professional": {
                    "organizations": [10, 19],
                    "events": [18, 5],
                    "description": "Professionals can join tech networks, co-working spaces, and career-focused events."
                },
                "investor": {
                    "organizations": [7, 11],
                    "events": [2, 17],
                    "description": "Investors can connect with startups through angel networks and pitch events."
                },
                "mentor": {
                    "organizations": [1, 2, 20],
                    "events": [25, 21],
                    "description": "Mentors can connect with entrepreneurs through mentorship programs and matchmaking events."
                }
            }
        ),
        Pathway(
            question="What is your biggest challenge right now?",
            answer_options={
                "validation": "Validating my idea",
                "funding": "Finding funding",
                "team": "Building a team",
                "customers": "Finding customers",
                "scaling": "Scaling my business"
            },
            recommended_resources={
                "validation": {
                    "organizations": [1, 8],
                    "events": [13, 23],
                    "description": "Join incubators and attend workshops on idea validation and customer discovery."
                },
                "funding": {
                    "organizations": [2, 7, 11],
                    "events": [2, 6, 17],
                    "description": "Explore accelerators, venture capital firms, angel networks, and funding workshops."
                },
                "team": {
                    "organizations": [10, 19],
                    "events": [18, 5, 21],
                    "description": "Network at tech events and co-working spaces to find co-founders and team members."
                },
                "customers": {
                    "organizations": [9, 14],
                    "events": [8, 15],
                    "description": "Business development centers and marketing workshops can help you find customers."
                },
                "scaling": {
                    "organizations": [2, 18],
                    "events": [14, 23],
                    "description": "Accelerators and export programs can help you scale your business effectively."
                }
            }
        ),
    ]
    
    for pathway in pathways:
        db.add(pathway)
    
    db.commit()  # Commit pathways to get IDs
    
    # Get organization IDs for programs (assuming organizations were created)
    org_list = db.query(Organization).all()
    if not org_list:
        print("⚠️  Warning: No organizations found. Programs will not be created.")
    else:
        # Seed Programs (15 programs)
        programs = [
            Program(
                title="Startup Accelerator Program",
                description="A 12-week intensive accelerator program for early-stage tech startups. Includes mentorship, funding opportunities, and access to investor network.",
                organization_id=org_list[1].id if len(org_list) > 1 else org_list[0].id,  # TechStart Windsor
                program_type="accelerator",
                stage="startup",
                sector="Technology",
                eligibility_criteria={"pre-revenue": True, "tech-focused": True},
                cost="Equity-based",
                duration="12 weeks",
                application_deadline=today + timedelta(days=30),
                start_date=today + timedelta(days=60),
                website="https://example.com/accelerator",
                application_link="https://example.com/accelerator/apply",
                is_verified=True,
                is_active=True
            ),
            Program(
                title="Women Entrepreneurs Mentorship Program",
                description="6-month mentorship program pairing women entrepreneurs with experienced business leaders. Includes monthly workshops and networking events.",
                organization_id=org_list[11].id if len(org_list) > 11 else org_list[0].id,  # Women Entrepreneurs Windsor
                program_type="mentorship",
                stage="idea",
                sector="All",
                eligibility_criteria={"women-led": True, "pre-revenue": True},
                cost="Free",
                duration="6 months",
                application_deadline=today + timedelta(days=20),
                start_date=today + timedelta(days=45),
                website="https://example.com/women-mentorship",
                application_link="https://example.com/women-mentorship/apply",
                is_verified=True,
                is_active=True
            ),
            Program(
                title="Student Entrepreneurship Incubator",
                description="Year-round incubator program for university and college students. Provides workspace, mentorship, and seed funding for student startups.",
                organization_id=org_list[3].id if len(org_list) > 3 else org_list[0].id,  # University of Windsor
                program_type="incubator",
                stage="idea",
                sector="All",
                eligibility_criteria={"student": True, "enrolled": True},
                cost="Free",
                duration="1 year",
                application_deadline=today + timedelta(days=45),
                start_date=today + timedelta(days=90),
                website="https://example.com/student-incubator",
                application_link="https://example.com/student-incubator/apply",
                is_verified=True,
                is_active=True
            ),
            Program(
                title="HealthTech Innovation Lab",
                description="Specialized program for health technology startups. Includes clinical partnerships, regulatory guidance, and access to healthcare networks.",
                organization_id=org_list[16].id if len(org_list) > 16 else org_list[0].id,  # HealthTech Accelerator
                program_type="accelerator",
                stage="startup",
                sector="Healthcare",
                eligibility_criteria={"healthtech": True, "early-stage": True},
                cost="Equity-based",
                duration="16 weeks",
                application_deadline=today + timedelta(days=25),
                start_date=today + timedelta(days=70),
                website="https://example.com/healthtech-lab",
                application_link="https://example.com/healthtech-lab/apply",
                is_verified=True,
                is_active=True
            ),
            Program(
                title="Export Readiness Training",
                description="Comprehensive 8-week program preparing businesses for international expansion. Covers market research, export regulations, and trade strategies.",
                organization_id=org_list[18].id if len(org_list) > 18 else org_list[0].id,  # Export Development Office
                program_type="workshop",
                stage="growth",
                sector="All",
                eligibility_criteria={"established": True, "export-ready": True},
                cost="Sliding scale",
                duration="8 weeks",
                application_deadline=today + timedelta(days=40),
                start_date=today + timedelta(days=80),
                website="https://example.com/export-training",
                application_link="https://example.com/export-training/apply",
                is_verified=False,
                is_active=True
            ),
            Program(
                title="GreenTech Startup Challenge",
                description="Competition and accelerator program for green technology startups. Winners receive funding, mentorship, and access to sustainability networks.",
                organization_id=org_list[7].id if len(org_list) > 7 else org_list[0].id,  # GreenTech Ventures
                program_type="accelerator",
                stage="idea",
                sector="GreenTech",
                eligibility_criteria={"greentech": True, "sustainable": True},
                cost="Free (competition)",
                duration="10 weeks",
                application_deadline=today + timedelta(days=15),
                start_date=today + timedelta(days=50),
                website="https://example.com/greentech-challenge",
                application_link="https://example.com/greentech-challenge/apply",
                is_verified=True,
                is_active=True
            ),
            Program(
                title="Food Innovation Kitchen Access",
                description="Program providing access to commercial kitchen facilities, food safety training, and regulatory guidance for food and beverage startups.",
                organization_id=org_list[15].id if len(org_list) > 15 else org_list[0].id,  # Food Innovation Centre
                program_type="incubator",
                stage="startup",
                sector="Food & Beverage",
                eligibility_criteria={"food-business": True},
                cost="Monthly fee",
                duration="Ongoing",
                application_deadline=None,
                start_date=None,
                website="https://example.com/food-kitchen",
                application_link="https://example.com/food-kitchen/apply",
                is_verified=False,
                is_active=True
            ),
            Program(
                title="Youth Entrepreneurship Bootcamp",
                description="Intensive 2-week bootcamp for young entrepreneurs aged 16-30. Covers ideation, business planning, and pitch preparation.",
                organization_id=org_list[17].id if len(org_list) > 17 else org_list[0].id,  # Youth Entrepreneurship Program
                program_type="workshop",
                stage="idea",
                sector="All",
                eligibility_criteria={"age": "16-30", "youth": True},
                cost="Free",
                duration="2 weeks",
                application_deadline=today + timedelta(days=35),
                start_date=today + timedelta(days=75),
                website="https://example.com/youth-bootcamp",
                application_link="https://example.com/youth-bootcamp/apply",
                is_verified=True,
                is_active=True
            ),
            Program(
                title="Manufacturing Innovation Program",
                description="Program supporting manufacturing startups with access to specialized equipment, industry expertise, and supply chain connections.",
                organization_id=org_list[13].id if len(org_list) > 13 else org_list[0].id,  # Manufacturing Innovation Hub
                program_type="incubator",
                stage="startup",
                sector="Manufacturing",
                eligibility_criteria={"manufacturing": True},
                cost="Membership-based",
                duration="6 months",
                application_deadline=today + timedelta(days=50),
                start_date=today + timedelta(days=100),
                website="https://example.com/manufacturing-program",
                application_link="https://example.com/manufacturing-program/apply",
                is_verified=False,
                is_active=True
            ),
            Program(
                title="Digital Media Creator Space",
                description="Co-working and incubation program for digital media creators, content creators, and creative tech startups.",
                organization_id=org_list[14].id if len(org_list) > 14 else org_list[0].id,  # Digital Media Lab
                program_type="incubator",
                stage="idea",
                sector="Digital Media",
                eligibility_criteria={"creative": True, "media-focused": True},
                cost="Sliding scale",
                duration="Ongoing",
                application_deadline=None,
                start_date=None,
                website="https://example.com/digital-media-space",
                application_link="https://example.com/digital-media-space/apply",
                is_verified=False,
                is_active=True
            ),
            Program(
                title="Angel Investor Network Membership",
                description="Exclusive membership program connecting entrepreneurs with angel investors. Includes pitch events, investor meetings, and deal flow access.",
                organization_id=org_list[11].id if len(org_list) > 11 else org_list[0].id,  # Angel Network
                program_type="network",
                stage="startup",
                sector="All",
                eligibility_criteria={"fundraising": True, "investor-ready": True},
                cost="Membership fee",
                duration="Annual",
                application_deadline=None,
                start_date=None,
                website="https://example.com/angel-network",
                application_link="https://example.com/angel-network/apply",
                is_verified=True,
                is_active=True
            ),
            Program(
                title="Business Model Validation Workshop",
                description="4-week intensive workshop helping entrepreneurs validate their business models through customer discovery and market testing.",
                organization_id=org_list[8].id if len(org_list) > 8 else org_list[0].id,  # Startup Foundry
                program_type="workshop",
                stage="idea",
                sector="All",
                eligibility_criteria={"pre-revenue": True},
                cost="Free",
                duration="4 weeks",
                application_deadline=today + timedelta(days=10),
                start_date=today + timedelta(days=30),
                website="https://example.com/business-validation",
                application_link="https://example.com/business-validation/apply",
                is_verified=False,
                is_active=True
            ),
            Program(
                title="TechBridge Professional Development",
                description="Ongoing professional development program for tech professionals. Includes workshops, networking, and career advancement resources.",
                organization_id=org_list[10].id if len(org_list) > 10 else org_list[0].id,  # TechBridge Windsor
                program_type="workshop",
                stage="growth",
                sector="Technology",
                eligibility_criteria={"tech-professional": True},
                cost="Membership-based",
                duration="Ongoing",
                application_deadline=None,
                start_date=None,
                website="https://example.com/techbridge-professional",
                application_link="https://example.com/techbridge-professional/apply",
                is_verified=False,
                is_active=True
            ),
            Program(
                title="Co-working Space Membership",
                description="Flexible co-working space membership with access to meeting rooms, networking events, and business support services.",
                organization_id=org_list[19].id if len(org_list) > 19 else org_list[0].id,  # Co-working Collective
                program_type="workspace",
                stage="All",
                sector="All",
                eligibility_criteria={},
                cost="Monthly fee",
                duration="Flexible",
                application_deadline=None,
                start_date=None,
                website="https://example.com/coworking-membership",
                application_link="https://example.com/coworking-membership/apply",
                is_verified=False,
                is_active=True
            ),
            Program(
                title="Innovation Zone Verified Program",
                description="Certification program for programs aligned with Innovation Zone goals. Provides verified status and increased visibility.",
                organization_id=org_list[0].id if len(org_list) > 0 else org_list[0].id,  # Innovation Hub
                program_type="certification",
                stage="All",
                sector="All",
                eligibility_criteria={"aligned": True, "quality": True},
                cost="Application fee",
                duration="Annual review",
                application_deadline=today + timedelta(days=60),
                start_date=None,
                website="https://example.com/verified-program",
                application_link="https://example.com/verified-program/apply",
                is_verified=True,
                is_active=True
            ),
        ]
        
        for program in programs:
            db.add(program)
        
        db.commit()
    
    total_items = len(events) + len(organizations) + len(pathways) + (len(programs) if org_list else 0)
    print("✅ Database seeded successfully!")
    print(f"   - {len(events)} events")
    print(f"   - {len(organizations)} organizations")
    print(f"   - {len(pathways)} pathways")
    if org_list:
        print(f"   - {len(programs)} programs")
    print(f"   - Total: {total_items} items")

except Exception as e:
    print(f"❌ Error seeding database: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
