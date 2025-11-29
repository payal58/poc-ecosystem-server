"""Seed pathways into the database"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal
from app.models import Pathway

def seed_pathways():
    """Seed 5 pathway questions"""
    db = SessionLocal()
    try:
        # Clear existing pathways
        db.query(Pathway).delete()
        db.commit()
        
        pathways = [
            Pathway(
                question="What stage is your business in?",
                answer_options={
                    "idea": "Idea",
                    "early": "Early Stage",
                    "growth": "Growing Business",
                    "established": "Established Business"
                },
                recommended_resources={}
            ),
            Pathway(
                question="What type of support are you looking for?",
                answer_options={
                    "funding": "Funding",
                    "mentorship": "Mentorship",
                    "networking": "Networking",
                    "training": "Training/Education"
                },
                recommended_resources={}
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
                recommended_resources={}
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
                recommended_resources={}
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
                recommended_resources={}
            ),
        ]
        
        for pathway in pathways:
            db.add(pathway)
        
        db.commit()
        print(f"✅ Seeded {len(pathways)} pathways")
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding pathways: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_pathways()


