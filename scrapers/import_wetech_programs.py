"""
Import WEtech Alliance scraped programs into the database
"""
import json
import os
import sys
import re
from datetime import datetime
from dateutil import parser as date_parser

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal
from app.models import Program, Organization

def find_or_create_wetech_org(db):
    """Find or create WEtech Alliance organization"""
    org = db.query(Organization).filter(
        Organization.organization_name.ilike('%WEtech%')
    ).first()
    
    if not org:
        # Create WEtech Alliance organization
        org = Organization(
            organization_name="WEtech Alliance",
            city="Windsor",
            province_state="ON",
            website="https://www.wetech-alliance.com/",
            email_address="info@wetech-alliance.com",
            sector_type="Technology, Innovation, Accelerator"
        )
        db.add(org)
        db.commit()
        db.refresh(org)
        print(f"✓ Created organization: {org.organization_name} (ID: {org.id})")
    else:
        print(f"✓ Found organization: {org.organization_name} (ID: {org.id})")
    
    return org

def parse_date(date_str):
    """Parse date string to date object"""
    if not date_str:
        return None
    try:
        # Try various date formats
        return date_parser.parse(date_str).date()
    except:
        return None

def is_valid_program(program_data):
    """Check if program data is valid (not a false positive)"""
    title = program_data.get('program_title', '').strip()
    url = program_data.get('program_page_url', '')
    
    # Skip invalid titles
    invalid_titles = [
        'OUR MISSION', 'HOME', 'CONTACT', 'ABOUT', 
        'BLOG', 'NEWS', 'EVENTS', 'TEAM'
    ]
    
    if title.upper() in invalid_titles:
        return False
    
    # Skip homepage
    if url == 'https://www.wetech-alliance.com/' or url == 'https://www.wetech-alliance.com':
        return False
    
    # Must have a title
    if not title or len(title) < 5:
        return False
    
    # Only include actual program pages, not news articles or blog posts
    # Valid program URLs should be:
    # - /scaleup/, /idea/, /blueprint/, /perks/, /jobs/, /wim/, /talks/, etc.
    # - NOT blog posts (/2025/..., /2024/..., /2023/...)
    # - NOT category pages (/category/...)
    # - NOT tag pages (/tag/...)
    # - NOT event pages (/event/...)
    
    url_lower = url.lower()
    
    # Exclude news/blog posts (dates in URL)
    if re.search(r'/\d{4}/\d{2}/', url_lower):
        return False
    
    # Exclude category pages
    if '/category/' in url_lower:
        return False
    
    # Exclude tag pages
    if '/tag/' in url_lower:
        return False
    
    # Exclude event pages (unless they're program-specific)
    if '/event/' in url_lower:
        return False
    
    # Include only actual program pages
    valid_program_paths = [
        '/scaleup', '/idea', '/blueprint', '/perks', '/jobs', 
        '/wim', '/talks', '/tech-connect', '/first-robotics',
        '/innovation-blueprint', '/client-perks', '/medhealth',
        '/women-in-mobility', '/tech-talks', '/tech-jobs'
    ]
    
    # Check if URL contains a valid program path
    is_program_page = any(path in url_lower for path in valid_program_paths)
    
    if not is_program_page:
        return False
    
    # Additional check: title should not be a quote or news headline
    if title.startswith('"') and title.endswith('"'):
        # Might be a quote from an article, skip it
        return False
    
    # Skip titles that look like dates
    if re.match(r'^\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', title):
        return False
    
    # Skip titles that are just dates
    if re.match(r'^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}', title, re.IGNORECASE):
        return False
    
    return True

def import_programs():
    """Import scraped programs into database"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, 'wetech_programs.json')
    
    if not os.path.exists(json_file):
        print(f"❌ Error: {json_file} not found")
        print("Please run wetech_scraper.py first to scrape programs.")
        return
    
    # Load scraped programs
    with open(json_file, 'r', encoding='utf-8') as f:
        scraped_programs = json.load(f)
    
    print(f"Loaded {len(scraped_programs)} scraped programs from JSON")
    
    db = SessionLocal()
    
    try:
        # Find or create WEtech Alliance organization
        wetech_org = find_or_create_wetech_org(db)
        
        imported_count = 0
        skipped_count = 0
        
        for scraped in scraped_programs:
            # Validate program
            if not is_valid_program(scraped):
                skipped_count += 1
                continue
            
            # Check if program already exists (by URL)
            existing = db.query(Program).filter(
                Program.website == scraped.get('program_page_url')
            ).first()
            
            if existing:
                print(f"  ⏭️  Skipping duplicate: {scraped.get('program_title', 'No title')[:60]}")
                skipped_count += 1
                continue
            
            # Determine program type from URL or title
            url_lower = scraped.get('program_page_url', '').lower()
            title_lower = scraped.get('program_title', '').lower()
            
            program_type = "program"  # default
            if 'accelerator' in url_lower or 'accelerator' in title_lower:
                program_type = "accelerator"
            elif 'fund' in url_lower or 'fund' in title_lower:
                program_type = "fund"
            elif 'grant' in url_lower or 'grant' in title_lower:
                program_type = "grant"
            elif 'workshop' in url_lower or 'workshop' in title_lower:
                program_type = "workshop"
            elif 'initiative' in url_lower or 'initiative' in title_lower:
                program_type = "initiative"
            
            # Extract dates
            deadline = parse_date(scraped.get('application_deadline'))
            start_date = parse_date(scraped.get('start_date'))
            
            # Create program
            program = Program(
                title=scraped.get('program_title', 'Untitled Program'),
                description=scraped.get('program_full_description') or scraped.get('program_summary') or 'No description available',
                organization_id=wetech_org.id,
                program_type=program_type,
                stage=None,  # Could be extracted from description
                sector=None,  # Could be extracted from description
                eligibility_criteria={
                    'eligibility': scraped.get('eligibility'),
                    'target_audience': scraped.get('target_audience')
                } if scraped.get('eligibility') or scraped.get('target_audience') else None,
                cost=None,  # Could be extracted from description
                duration=None,  # Could be extracted from description
                application_deadline=deadline,
                start_date=start_date,
                website=scraped.get('program_page_url'),
                application_link=scraped.get('program_page_url'),  # Use same URL as application link
                is_verified=True,  # WEtech Alliance is a verified organization
                is_active=True
            )
            
            db.add(program)
            imported_count += 1
            print(f"  ✓ Importing: {program.title[:60]}")
        
        db.commit()
        
        print(f"\n✅ Import complete!")
        print(f"   - Imported: {imported_count} programs")
        print(f"   - Skipped: {skipped_count} programs (invalid or duplicates)")
        
    except Exception as e:
        print(f"❌ Error importing programs: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_programs()

