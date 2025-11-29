"""Import Invest WindsorEssex Foreign Trade Zone programs into the database"""
import json
import os
import sys
from sqlalchemy import delete

# Ensure app modules are importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal
from app.models import Program, Organization

ORG_NAME = "Invest WindsorEssex"
ORG_WEBSITE = "https://www.investwindsoressex.com/"


def get_or_create_org(db):
    """Get or create Invest WindsorEssex organization"""
    org = (
        db.query(Organization)
        .filter(Organization.organization_name.ilike('%invest windsor%'))
        .first()
    )
    if org:
        return org

    org = Organization(
        organization_name=ORG_NAME,
        city="Windsor",
        address="119 Chatham St. W, Unit #100",
        province_state="ON",
        website=ORG_WEBSITE,
        phone_number="519.255.9200",
        notes="Foreign Trade Zone Programs scraped from Invest WindsorEssex website",
    )
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


def import_programs():
    """Import scraped programs into the database"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, 'invest_windsor_programs.json')

    if not os.path.exists(data_file):
        print(f"❌ Missing {data_file}. Run invest_windsor_scraper.py first.")
        return

    with open(data_file, 'r', encoding='utf-8') as f:
        programs = json.load(f)

    db = SessionLocal()
    try:
        org = get_or_create_org(db)
        print(f"✅ Using organization: {org.organization_name} (ID: {org.id})")

        # Clear existing Invest WindsorEssex programs to avoid duplicates
        deleted = db.execute(delete(Program).where(Program.organization_id == org.id))
        db.commit()
        if deleted.rowcount:
            print(f"🗑️  Cleared {deleted.rowcount} existing programs")

        imported = 0
        for program in programs:
            description = program.get('program_description') or 'See program website for full details.'
            application_link = program.get('application_link') or program.get('program_page_url')
            
            new_program = Program(
                title=program.get('program_title'),
                description=description,
                organization_id=org.id,
                program_type=program.get('program_type') or 'foreign trade zone program',
                website=program.get('program_page_url'),
                application_link=application_link,
                is_active=True,
                is_verified=False,
            )
            db.add(new_program)
            imported += 1

        db.commit()
        print(f"✅ Imported {imported} Invest WindsorEssex programs")
    except Exception as exc:
        db.rollback()
        print("❌ Error importing programs:", exc)
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import_programs()
