"""Categorize all existing programs into business stages"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal
from app.models import Program
from app.utils.program_categorizer import categorize_program_stage, get_stage_display_name


def categorize_all_programs():
    """Update all programs with appropriate business stages"""
    db = SessionLocal()
    try:
        programs = db.query(Program).all()
        print(f"Found {len(programs)} programs to categorize")
        
        updated = 0
        unchanged = 0
        no_match = 0
        
        for program in programs:
            # Get current stage
            current_stage = program.stage
            
            # Categorize based on title and description
            new_stage = categorize_program_stage(program.title, program.description)
            
            if new_stage:
                # Normalize the stage name
                normalized_stage = get_stage_display_name(new_stage)
                
                # Update if different
                if normalized_stage != current_stage:
                    program.stage = normalized_stage
                    updated += 1
                    print(f"✓ Updated '{program.title}': {current_stage or 'None'} → {normalized_stage}")
                else:
                    unchanged += 1
            else:
                no_match += 1
                print(f"⚠ No match for '{program.title}'")
        
        db.commit()
        
        print(f"\n✅ Categorization complete:")
        print(f"   - Updated: {updated}")
        print(f"   - Unchanged: {unchanged}")
        print(f"   - No match: {no_match}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    categorize_all_programs()

