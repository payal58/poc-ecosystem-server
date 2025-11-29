"""
Update program descriptions with cleaned versions
"""
import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal
from app.models import Program, Organization

def update_descriptions():
    """Update program descriptions"""
    db = SessionLocal()
    
    try:
        # Load scraped data
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(script_dir, 'wetech_programs.json')
        with open(json_file, 'r', encoding='utf-8') as f:
            scraped = json.load(f)
        
        wetech = db.query(Organization).filter(
            Organization.organization_name.ilike('%WEtech%')
        ).first()
        
        if not wetech:
            print("WEtech Alliance organization not found")
            return
        
        # Create mapping of URL to description
        url_to_data = {p['program_page_url']: p for p in scraped}
        
        programs = db.query(Program).filter(Program.organization_id == wetech.id).all()
        updated_count = 0
        
        for program in programs:
            url = program.website or ''
            if url in url_to_data:
                scraped_data = url_to_data[url]
                new_description = scraped_data.get('program_full_description') or scraped_data.get('program_summary') or ''
                
                if new_description and program.description != new_description:
                    print(f"Updating description for: {program.title}")
                    program.description = new_description
                    updated_count += 1
        
        db.commit()
        print(f"\n✅ Updated {updated_count} program descriptions")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_descriptions()
