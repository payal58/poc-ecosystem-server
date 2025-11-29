"""Utility to categorize programs into business stages based on their descriptions"""
import re
from typing import Optional

# Define stage categories and their keywords
STAGE_KEYWORDS = {
    "Idea / Inspiration": [
        "idea", "inspiration", "brainstorm", "problem", "opportunity", "explore",
        "discover", "identify", "concept", "initial", "early stage", "pre-idea",
        "ideation", "thinking", "exploring", "discovery", "opportunities"
    ],
    "Validation": [
        "validate", "validation", "market research", "customer research", "feasibility",
        "test market", "market validation", "customer validation", "demand",
        "need", "problem validation", "research", "survey", "interview",
        "market analysis", "competitive analysis", "validate idea"
    ],
    "Concept Development": [
        "concept", "prototype", "design", "develop concept", "shape idea",
        "solution design", "business model", "value proposition", "pitch",
        "business plan", "strategy", "planning", "framework", "blueprint",
        "develop solution", "conceptualize", "design thinking"
    ],
    "MVP / Testing": [
        "mvp", "minimum viable product", "test", "testing", "pilot", "beta",
        "prototype", "build", "develop", "create", "build product", "develop product",
        "user testing", "product development", "build mvp", "test product",
        "pilot program", "beta testing", "user feedback", "iterate"
    ],
    "Business Setup": [
        "setup", "incorporate", "legal", "registration", "business registration",
        "incorporation", "business license", "tax", "accounting", "bookkeeping",
        "business structure", "legal structure", "operational", "operations",
        "business model", "formalize", "establish", "register business",
        "business formation", "company setup", "start business"
    ],
    "Launch": [
        "launch", "go to market", "market entry", "introduce", "release",
        "debut", "unveil", "rollout", "market launch", "product launch",
        "service launch", "commercial launch", "go live", "enter market"
    ],
    "Growth": [
        "growth", "scale", "scaling", "expand", "expansion", "scale up",
        "grow business", "increase revenue", "market expansion", "scale business",
        "accelerate", "accelerator", "growth stage", "scaling up", "expand market",
        "business growth", "revenue growth", "customer acquisition", "scale operations"
    ]
}


def categorize_program_stage(title: str, description: str) -> Optional[str]:
    """
    Categorize a program into a business stage based on title and description.
    
    Args:
        title: Program title
        description: Program description
        
    Returns:
        Stage name or None if no match found
    """
    if not description:
        return None
    
    # Combine title and description for analysis
    text = f"{title} {description}".lower()
    
    # Score each stage based on keyword matches
    stage_scores = {}
    
    for stage, keywords in STAGE_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            # Count occurrences (case-insensitive)
            count = len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', text))
            score += count
        
        if score > 0:
            stage_scores[stage] = score
    
    # Return the stage with the highest score
    if stage_scores:
        return max(stage_scores, key=stage_scores.get)
    
    # Fallback: Check for specific program types that indicate stages
    text_lower = text.lower()
    
    # Accelerators and incubators often target early stages
    if any(word in text_lower for word in ["accelerator", "incubator", "startup"]):
        if any(word in text_lower for word in ["early", "idea", "concept"]):
            return "Idea / Inspiration"
        elif any(word in text_lower for word in ["validate", "validation", "research"]):
            return "Validation"
        else:
            return "Concept Development"
    
    # Mentorship programs often span multiple stages
    if "mentorship" in text_lower or "mentor" in text_lower:
        if any(word in text_lower for word in ["early", "idea", "starting"]):
            return "Idea / Inspiration"
        elif any(word in text_lower for word in ["growth", "scale", "expand"]):
            return "Growth"
        else:
            return "Concept Development"
    
    # Workshops and training
    if any(word in text_lower for word in ["workshop", "training", "seminar"]):
        if any(word in text_lower for word in ["idea", "brainstorm", "explore"]):
            return "Idea / Inspiration"
        elif any(word in text_lower for word in ["validate", "research", "market"]):
            return "Validation"
        elif any(word in text_lower for word in ["launch", "go to market"]):
            return "Launch"
        elif any(word in text_lower for word in ["growth", "scale"]):
            return "Growth"
        else:
            return "Concept Development"
    
    # Funding and grants
    if any(word in text_lower for word in ["fund", "grant", "financing", "loan"]):
        if any(word in text_lower for word in ["early", "startup", "seed"]):
            return "Concept Development"
        elif any(word in text_lower for word in ["growth", "scale", "expansion"]):
            return "Growth"
        else:
            return "Business Setup"
    
    # If no clear match, return None
    return None


def get_stage_display_name(stage: Optional[str]) -> Optional[str]:
    """Get the display name for a stage (for consistency)"""
    if not stage:
        return None
    
    # Normalize stage names
    stage_lower = stage.lower()
    
    # Map variations to standard names
    stage_map = {
        "idea": "Idea / Inspiration",
        "inspiration": "Idea / Inspiration",
        "idea / inspiration": "Idea / Inspiration",
        "validation": "Validation",
        "concept": "Concept Development",
        "concept development": "Concept Development",
        "mvp": "MVP / Testing",
        "testing": "MVP / Testing",
        "mvp / testing": "MVP / Testing",
        "setup": "Business Setup",
        "business setup": "Business Setup",
        "launch": "Launch",
        "growth": "Growth",
        "scale": "Growth",
    }
    
    # Check exact match first
    if stage in STAGE_KEYWORDS:
        return stage
    
    # Check normalized match
    for key, value in stage_map.items():
        if key in stage_lower:
            return value
    
    return stage  # Return as-is if no match

