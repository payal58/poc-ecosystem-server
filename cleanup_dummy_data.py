"""
Remove dummy data and keep only real scraped data
Run: python cleanup_dummy_data.py
"""
from app.database import SessionLocal
from app.models import Organization, Program

db = SessionLocal()

try:
    # Real organizations (created by import scripts)
    real_org_ids = [378, 379, 380]  # Invest WindsorEssex, SBEC, WEtech Alliance
    
    # Get real organizations to verify they exist
    real_orgs = db.query(Organization).filter(Organization.id.in_(real_org_ids)).all()
    print(f"✅ Found {len(real_orgs)} real organizations:")
    for org in real_orgs:
        print(f"   - {org.organization_name} (ID: {org.id})")
    
    # Count dummy programs (programs not from real organizations)
    dummy_programs = db.query(Program).filter(~Program.organization_id.in_(real_org_ids)).all()
    print(f"\n🗑️  Removing {len(dummy_programs)} dummy programs...")
    for program in dummy_programs:
        db.delete(program)
    db.commit()
    print(f"✅ Removed {len(dummy_programs)} dummy programs")
    
    # Count dummy organizations (organizations that are not real and have no programs)
    dummy_orgs = db.query(Organization).filter(~Organization.id.in_(real_org_ids)).all()
    print(f"\n🗑️  Removing {len(dummy_orgs)} dummy organizations...")
    for org in dummy_orgs:
        db.delete(org)
    db.commit()
    print(f"✅ Removed {len(dummy_orgs)} dummy organizations")
    
    # Final summary
    print(f"\n✅ Cleanup complete!")
    print(f"   Real Organizations: {db.query(Organization).count()}")
    print(f"   Real Programs: {db.query(Program).count()}")
    
    # Show final programs
    all_programs = db.query(Program).join(Organization).all()
    print(f"\n📋 Real Programs in database:")
    for program in all_programs:
        print(f"   - {program.title[:60]} ({program.organization.organization_name})")
    
except Exception as e:
    print(f"❌ Error cleaning up: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()

