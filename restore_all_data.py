"""
Comprehensive script to restore all data (organizations, events, programs, pathways)
Uses the current database schema
Run: python restore_all_data.py
"""
from app.database import SessionLocal
from app.models import Event, Organization, Program, Pathway
from datetime import date, timedelta

db = SessionLocal()

try:
    print("🔄 Starting data restoration...")
    
    # Check current counts
    org_count = db.query(Organization).count()
    event_count = db.query(Event).count()
    program_count = db.query(Program).count()
    pathway_count = db.query(Pathway).count()
    
    print(f"\nCurrent database state:")
    print(f"  Organizations: {org_count}")
    print(f"  Events: {event_count}")
    print(f"  Programs: {program_count}")
    print(f"  Pathways: {pathway_count}")
    
    # Restore Organizations (20 organizations with current schema)
    if org_count < 20:
        print(f"\n📦 Restoring organizations...")
        # Clear existing if needed (delete in correct order to handle foreign keys)
        if org_count > 0:
            # Delete programs first (they reference organizations)
            db.query(Program).delete()
            db.commit()
            # Now delete organizations
            db.query(Organization).delete()
            db.commit()
        
        organizations = [
            Organization(
                organization_name="Windsor-Essex Innovation Hub",
                city="Windsor",
                address="123 Innovation Drive",
                province_state="Ontario",
                sector_type="Innovation & Technology",
                services_offered="Startup support, mentorship programs, co-working space, funding opportunities",
                website="https://example.com/innovation-hub",
                email_address="info@innovationhub.com",
                phone_number="(519) 555-0100",
                contact_name="Innovation Hub Team",
                notes="Leading innovation center supporting startups and entrepreneurs in the region."
            ),
            Organization(
                organization_name="TechStart Windsor",
                city="Windsor",
                address="456 Tech Avenue",
                province_state="Ontario",
                sector_type="Accelerator",
                services_offered="Accelerator program, mentorship, funding opportunities, investor network",
                website="https://example.com/techstart",
                email_address="contact@techstart.com",
                phone_number="(519) 555-0101",
                contact_name="TechStart Team"
            ),
            Organization(
                organization_name="Entrepreneur Network Windsor",
                city="Windsor",
                address="789 Business Blvd",
                province_state="Ontario",
                sector_type="Network",
                services_offered="Networking events, community support, knowledge sharing",
                website="https://example.com/entrepreneur-network",
                email_address="hello@entnetwork.com",
                phone_number="(519) 555-0102",
                contact_name="Network Coordinator"
            ),
            Organization(
                organization_name="University of Windsor - Innovation Centre",
                city="Windsor",
                address="401 Sunset Avenue",
                province_state="Ontario",
                sector_type="University",
                services_offered="Student entrepreneurship, research facilities, mentorship",
                website="https://example.com/uwindsor-innovation",
                email_address="innovation@uwindsor.ca",
                phone_number="(519) 555-0103",
                contact_name="Innovation Centre Director"
            ),
            Organization(
                organization_name="St. Clair College - Entrepreneurship Program",
                city="Windsor",
                address="2000 Talbot Road",
                province_state="Ontario",
                sector_type="College",
                services_offered="Entrepreneurship courses, mentorship, startup support",
                website="https://example.com/stclair-entrepreneurship",
                email_address="entrepreneurship@stclaircollege.ca",
                phone_number="(519) 555-0104",
                contact_name="Program Coordinator"
            ),
            Organization(
                organization_name="Windsor-Essex Economic Development Corporation",
                city="Windsor",
                address="100 Ouellette Avenue",
                province_state="Ontario",
                sector_type="Economic Development",
                services_offered="Economic development initiatives, funding programs, business advisory",
                website="https://example.com/we-edc",
                email_address="info@we-edc.ca",
                phone_number="(519) 555-0105",
                contact_name="Economic Development Officer"
            ),
            Organization(
                organization_name="GreenTech Ventures",
                city="Windsor",
                address="321 Green Street",
                province_state="Ontario",
                sector_type="Venture Capital",
                services_offered="Venture capital, green technology investment, startup funding",
                website="https://example.com/greentech-ventures",
                email_address="invest@greentechventures.com",
                phone_number="(519) 555-0106",
                contact_name="Investment Team"
            ),
            Organization(
                organization_name="Windsor Startup Foundry",
                city="Windsor",
                address="654 Startup Lane",
                province_state="Ontario",
                sector_type="Incubator",
                services_offered="Early-stage incubator, workspace, mentorship, investor network",
                website="https://example.com/startup-foundry",
                email_address="info@startupfoundry.ca",
                phone_number="(519) 555-0107",
                contact_name="Foundry Director"
            ),
            Organization(
                organization_name="Windsor Business Development Centre",
                city="Windsor",
                address="987 Commerce Way",
                province_state="Ontario",
                sector_type="Consulting",
                services_offered="Business development, market research, business planning, growth strategies",
                website="https://example.com/business-dev",
                email_address="info@bizdevcentre.ca",
                phone_number="(519) 555-0108",
                contact_name="Business Development Advisor"
            ),
            Organization(
                organization_name="TechBridge Windsor",
                city="Windsor",
                address="147 Tech Bridge Road",
                province_state="Ontario",
                sector_type="Network",
                services_offered="Tech networking, workshops, career development, talent connection",
                website="https://example.com/techbridge",
                email_address="hello@techbridge.ca",
                phone_number="(519) 555-0109",
                contact_name="TechBridge Coordinator"
            ),
            Organization(
                organization_name="Windsor Angel Network",
                city="Windsor",
                address="258 Investment Plaza",
                province_state="Ontario",
                sector_type="Investment",
                services_offered="Angel investment, pitch events, investor connections",
                website="https://example.com/angel-network",
                email_address="info@angelnetwork.ca",
                phone_number="(519) 555-0110",
                contact_name="Angel Network Manager"
            ),
            Organization(
                organization_name="Women Entrepreneurs Windsor",
                city="Windsor",
                address="369 Women's Business Center",
                province_state="Ontario",
                sector_type="Network",
                services_offered="Women entrepreneur support, mentorship, networking, business development",
                website="https://example.com/women-entrepreneurs",
                email_address="contact@womenentrepreneurs.ca",
                phone_number="(519) 555-0111",
                contact_name="Program Director"
            ),
            Organization(
                organization_name="Windsor Manufacturing Innovation Hub",
                city="Windsor",
                address="741 Manufacturing Drive",
                province_state="Ontario",
                sector_type="Manufacturing",
                services_offered="Manufacturing startup support, specialized equipment, industry expertise",
                website="https://example.com/manufacturing-hub",
                email_address="info@manufacturinghub.ca",
                phone_number="(519) 555-0112",
                contact_name="Hub Manager"
            ),
            Organization(
                organization_name="Windsor Digital Media Lab",
                city="Windsor",
                address="852 Creative Avenue",
                province_state="Ontario",
                sector_type="Creative",
                services_offered="Digital media co-working, creative tech incubation, content creation support",
                website="https://example.com/digital-media-lab",
                email_address="info@digitalmedialab.ca",
                phone_number="(519) 555-0113",
                contact_name="Lab Director"
            ),
            Organization(
                organization_name="Windsor Food Innovation Centre",
                city="Windsor",
                address="963 Food Street",
                province_state="Ontario",
                sector_type="Food & Beverage",
                services_offered="Commercial kitchen access, food safety training, regulatory guidance",
                website="https://example.com/food-innovation",
                email_address="info@foodinnovation.ca",
                phone_number="(519) 555-0114",
                contact_name="Centre Manager"
            ),
            Organization(
                organization_name="Windsor HealthTech Accelerator",
                city="Windsor",
                address="159 Health Tech Boulevard",
                province_state="Ontario",
                sector_type="Healthcare",
                services_offered="HealthTech acceleration, clinical partnerships, regulatory support",
                website="https://example.com/healthtech-accelerator",
                email_address="info@healthtech.ca",
                phone_number="(519) 555-0115",
                contact_name="Accelerator Director"
            ),
            Organization(
                organization_name="Windsor Youth Entrepreneurship Program",
                city="Windsor",
                address="357 Youth Center Drive",
                province_state="Ontario",
                sector_type="Education",
                services_offered="Youth entrepreneurship support, workshops, startup funding for ages 16-30",
                website="https://example.com/youth-entrepreneurship",
                email_address="youth@entrepreneurship.ca",
                phone_number="(519) 555-0116",
                contact_name="Youth Program Coordinator"
            ),
            Organization(
                organization_name="Windsor Export Development Office",
                city="Windsor",
                address="468 Export Way",
                province_state="Ontario",
                sector_type="Export Services",
                services_offered="Export programs, trade missions, market intelligence, international expansion support",
                website="https://example.com/export-office",
                email_address="export@windsor.ca",
                phone_number="(519) 555-0117",
                contact_name="Export Development Officer"
            ),
            Organization(
                organization_name="Windsor Co-working Collective",
                city="Windsor",
                address="579 Co-working Square",
                province_state="Ontario",
                sector_type="Co-working",
                services_offered="Co-working space, meeting rooms, networking events, business support",
                website="https://example.com/coworking",
                email_address="info@coworkingcollective.ca",
                phone_number="(519) 555-0118",
                contact_name="Community Manager"
            ),
            Organization(
                organization_name="Windsor Innovation Alliance",
                city="Windsor",
                address="680 Alliance Drive",
                province_state="Ontario",
                sector_type="Network",
                services_offered="Innovation ecosystem connection, networking, collaboration facilitation",
                website="https://example.com/innovation-alliance",
                email_address="info@innovationalliance.ca",
                phone_number="(519) 555-0119",
                contact_name="Alliance Director"
            ),
        ]
        
        for org in organizations:
            db.add(org)
        
        db.commit()
        print(f"✅ Restored {len(organizations)} organizations")
    
    # Restore Events (25 events)
    if event_count < 25:
        print(f"\n📅 Restoring events...")
        if event_count > 0:
            db.query(Event).delete()
            db.commit()
        
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
        print(f"✅ Restored {len(events)} events")
    
    # Restore Pathways (5 pathways)
    if pathway_count < 5:
        print(f"\n🛤️  Restoring pathways...")
        if pathway_count > 0:
            db.query(Pathway).delete()
            db.commit()
        
        # Get organization IDs for pathways (use first few orgs)
        org_list = db.query(Organization).limit(20).all()
        org_ids = [org.id for org in org_list] if org_list else list(range(1, 21))
        
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
                        "organizations": org_ids[:3] if len(org_ids) >= 3 else [1, 2, 3],
                        "events": [1, 2, 13],
                        "description": "Consider joining our incubator program or attending networking events to validate your idea."
                    },
                    "early": {
                        "organizations": org_ids[:3] if len(org_ids) >= 3 else [1, 2, 3],
                        "events": [2, 13, 16],
                        "description": "Accelerator programs and pitch events would be beneficial for early-stage startups."
                    },
                    "growth": {
                        "organizations": org_ids[1:4] if len(org_ids) >= 4 else [2, 3, 4],
                        "events": [1, 2, 6],
                        "description": "Focus on scaling and connecting with investors to fuel your growth."
                    },
                    "established": {
                        "organizations": org_ids[2:5] if len(org_ids) >= 5 else [3, 4, 5],
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
                        "organizations": org_ids[6:9] if len(org_ids) >= 9 else [7, 8, 9],
                        "events": [2, 17, 6],
                        "description": "Check out our accelerator program, angel investor network, and pitch events for funding opportunities."
                    },
                    "mentorship": {
                        "organizations": org_ids[:3] if len(org_ids) >= 3 else [1, 2, 3],
                        "events": [25, 21],
                        "description": "Incubators, accelerators, and mentorship programs offer structured mentorship opportunities."
                    },
                    "networking": {
                        "organizations": org_ids[2:5] if len(org_ids) >= 5 else [3, 4, 5],
                        "events": [5, 12, 21, 24],
                        "description": "Join networking events and entrepreneur communities to build your professional network."
                    },
                    "training": {
                        "organizations": org_ids[3:6] if len(org_ids) >= 6 else [4, 5, 6],
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
                        "organizations": org_ids[1:4] if len(org_ids) >= 4 else [2, 3, 4],
                        "events": [1, 4, 18],
                        "description": "Tech-focused accelerators and networking events are perfect for technology startups."
                    },
                    "health": {
                        "organizations": org_ids[15:16] if len(org_ids) >= 16 else [16],
                        "events": [11],
                        "description": "HealthTech accelerator provides specialized support for healthcare technology startups."
                    },
                    "green": {
                        "organizations": org_ids[6:7] if len(org_ids) >= 7 else [7],
                        "events": [7],
                        "description": "GreenTech Ventures specializes in sustainable innovation and green technology."
                    },
                    "food": {
                        "organizations": org_ids[14:15] if len(org_ids) >= 15 else [15],
                        "events": [15],
                        "description": "Food Innovation Centre offers specialized support for food and beverage startups."
                    },
                    "manufacturing": {
                        "organizations": org_ids[12:13] if len(org_ids) >= 13 else [13],
                        "events": [10],
                        "description": "Manufacturing Innovation Hub provides specialized equipment and industry expertise."
                    },
                    "media": {
                        "organizations": org_ids[13:14] if len(org_ids) >= 14 else [14],
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
                        "organizations": org_ids[:4] if len(org_ids) >= 4 else [1, 2, 3, 4],
                        "events": [2, 5, 21, 13],
                        "description": "As a founder, connect with incubators, accelerators, and networking events to grow your startup."
                    },
                    "student": {
                        "organizations": org_ids[3:6] if len(org_ids) >= 6 else [4, 5, 6],
                        "events": [9, 16, 18],
                        "description": "Students can benefit from university programs, youth entrepreneurship programs, and student-focused events."
                    },
                    "professional": {
                        "organizations": org_ids[9:11] if len(org_ids) >= 11 else [10, 11],
                        "events": [18, 5],
                        "description": "Professionals can join tech networks, co-working spaces, and career-focused events."
                    },
                    "investor": {
                        "organizations": org_ids[6:8] if len(org_ids) >= 8 else [7, 8],
                        "events": [2, 17],
                        "description": "Investors can connect with startups through angel networks and pitch events."
                    },
                    "mentor": {
                        "organizations": org_ids[:3] if len(org_ids) >= 3 else [1, 2, 3],
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
                        "organizations": org_ids[:2] if len(org_ids) >= 2 else [1, 2],
                        "events": [13, 23],
                        "description": "Join incubators and attend workshops on idea validation and customer discovery."
                    },
                    "funding": {
                        "organizations": org_ids[1:4] if len(org_ids) >= 4 else [2, 3, 4],
                        "events": [2, 6, 17],
                        "description": "Explore accelerators, venture capital firms, angel networks, and funding workshops."
                    },
                    "team": {
                        "organizations": org_ids[9:11] if len(org_ids) >= 11 else [10, 11],
                        "events": [18, 5, 21],
                        "description": "Network at tech events and co-working spaces to find co-founders and team members."
                    },
                    "customers": {
                        "organizations": org_ids[8:10] if len(org_ids) >= 10 else [9, 10],
                        "events": [8, 15],
                        "description": "Business development centers and marketing workshops can help you find customers."
                    },
                    "scaling": {
                        "organizations": org_ids[1:3] if len(org_ids) >= 3 else [2, 3],
                        "events": [14, 23],
                        "description": "Accelerators and export programs can help you scale your business effectively."
                    }
                }
            ),
        ]
        
        for pathway in pathways:
            db.add(pathway)
        
        db.commit()
        print(f"✅ Restored {len(pathways)} pathways")
    
    # Restore Programs (15 programs) - Note: This runs after organizations are restored
    print(f"\n📚 Restoring programs...")
    # Delete existing programs first (they reference organizations)
    existing_programs = db.query(Program).count()
    if existing_programs > 0:
        db.query(Program).delete()
        db.commit()
        print(f"   Cleared {existing_programs} existing programs")
    
    # Get organization IDs for programs
    org_list = db.query(Organization).all()
    if not org_list or len(org_list) < 2:
        print("⚠️  Warning: Not enough organizations. Programs will use placeholder IDs.")
        org_ids = list(range(1, 21))
    else:
        org_ids = [org.id for org in org_list]
    
    today = date.today()
    programs = [
        Program(
                title="Startup Accelerator Program",
                description="A 12-week intensive accelerator program for early-stage tech startups. Includes mentorship, funding opportunities, and access to investor network.",
                organization_id=org_ids[1] if len(org_ids) > 1 else org_ids[0],
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
                organization_id=org_ids[11] if len(org_ids) > 11 else org_ids[0],
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
                organization_id=org_ids[3] if len(org_ids) > 3 else org_ids[0],
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
                organization_id=org_ids[15] if len(org_ids) > 15 else org_ids[0],
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
                organization_id=org_ids[17] if len(org_ids) > 17 else org_ids[0],
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
                organization_id=org_ids[6] if len(org_ids) > 6 else org_ids[0],
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
                organization_id=org_ids[14] if len(org_ids) > 14 else org_ids[0],
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
                organization_id=org_ids[16] if len(org_ids) > 16 else org_ids[0],
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
                organization_id=org_ids[12] if len(org_ids) > 12 else org_ids[0],
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
                organization_id=org_ids[13] if len(org_ids) > 13 else org_ids[0],
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
                organization_id=org_ids[10] if len(org_ids) > 10 else org_ids[0],
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
                organization_id=org_ids[7] if len(org_ids) > 7 else org_ids[0],
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
                organization_id=org_ids[9] if len(org_ids) > 9 else org_ids[0],
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
                organization_id=org_ids[18] if len(org_ids) > 18 else org_ids[0],
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
                organization_id=org_ids[0] if len(org_ids) > 0 else org_ids[0],
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
    print(f"✅ Restored {len(programs)} programs")
    
    # Final summary
    print(f"\n✅ Data restoration complete!")
    print(f"\nFinal database state:")
    print(f"  Organizations: {db.query(Organization).count()}")
    print(f"  Events: {db.query(Event).count()}")
    print(f"  Programs: {db.query(Program).count()}")
    print(f"  Pathways: {db.query(Pathway).count()}")
    
except Exception as e:
    print(f"❌ Error restoring data: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()

