"""Import SBEC programs into the database"""
import json
import os
import sys
from sqlalchemy import delete

# Ensure app modules are importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal
from app.models import Program, Organization

SBEC_NAME = "Small Business & Entrepreneurship Centre"
SBEC_WEBSITE = "https://www.webusinesscentre.com/"


def get_or_create_sbec_org(db):
    org = (
        db.query(Organization)
        .filter(Organization.organization_name.ilike('%small business%entrepreneurship centre%'))
        .first()
    )
    if org:
        return org

    org = Organization(
        organization_name=SBEC_NAME,
        city="Windsor",
        address="119 Chatham St. W, Unit 100",
        province_state="ON",
        website=SBEC_WEBSITE,
        phone_number="519-253-6900",
        notes="Programs scraped from SBEC Programs and Financial Support page",
    )
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


def import_programs():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, 'sbec_programs.json')

    if not os.path.exists(data_file):
        print(f"❌ Missing {data_file}. Run sbec_scraper.py first.")
        return

    with open(data_file, 'r', encoding='utf-8') as f:
        programs = json.load(f)

    db = SessionLocal()
    try:
        sbec_org = get_or_create_sbec_org(db)

        # Clear existing SBEC programs to avoid duplicates
        db.execute(delete(Program).where(Program.organization_id == sbec_org.id))
        db.commit()

        imported = 0
        for program in programs:
            description = program.get('program_description') or 'See program website for full details.'
            application_link = program.get('application_link') or program.get('program_page_url')
            new_program = Program(
                title=program.get('program_title'),
                description=description,
                organization_id=sbec_org.id,
                program_type=program.get('program_type') or 'program',
                website=program.get('program_page_url'),
                application_link=application_link,
                is_active=True,
                is_verified=False,
            )
            db.add(new_program)
            imported += 1

        db.commit()
        print(f"✅ Imported {imported} SBEC programs")
    except Exception as exc:
        db.rollback()
        print("❌ Error importing programs:", exc)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import_programs()
