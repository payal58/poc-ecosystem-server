"""Remove non-WEtech/SBEC programs"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import delete
from app.database import SessionLocal
from app.models import Program, Organization

ALLOWED_NAMES = [
    '%wetech alliance%',
    '%small business%entrepreneurship centre%'
]

def get_allowed_ids(db):
    ids = []
    for pattern in ALLOWED_NAMES:
        org = (
            db.query(Organization)
            .filter(Organization.organization_name.ilike(pattern))
            .first()
        )
        if org:
            ids.append(org.id)
    return ids

def run():
    db = SessionLocal()
    try:
        allowed = get_allowed_ids(db)
        if not allowed:
            print('No matching organizations found. Aborting.')
            return
        print('Keeping programs for org IDs:', allowed)
        deleted = db.execute(
            delete(Program).where(~Program.organization_id.in_(allowed))
        )
        db.commit()
        print(f"Deleted {deleted.rowcount or 0} programs outside allowed organizations")
    finally:
        db.close()

if __name__ == '__main__':
    run()
