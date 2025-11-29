"""
Gemini AI service for pathway recommendations
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Dict, List, Any
from app.models import Pathway, Organization, Event, Program
from sqlalchemy.orm import Session

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def build_system_prompt(pathways: List[Pathway], organizations: List[Organization], events: List[Event], programs: List[Program]) -> str:
    """Build a comprehensive system prompt with all database information"""
    
    prompt = """You are an AI assistant for the Windsor-Essex Innovation Zone Ecosystem Platform. 
Your role is to provide personalized recommendations to users based on their responses to pathway questions.

You MUST only use information from the database provided below. Do not make up or suggest resources that are not in the database.

DATABASE INFORMATION:

=== PATHWAYS ===
"""
    
    # Add all pathways
    for pathway in pathways:
        prompt += f"\nPathway ID: {pathway.id}\n"
        prompt += f"Question: {pathway.question}\n"
        if pathway.answer_options:
            prompt += "Answer Options:\n"
            for key, value in pathway.answer_options.items():
                prompt += f"  - {key}: {value}\n"
        if pathway.recommended_resources:
            prompt += "Recommended Resources:\n"
            prompt += f"{pathway.recommended_resources}\n"
        prompt += "\n"
    
    prompt += "\n=== ORGANIZATIONS ===\n"
    # Add all organizations
    for org in organizations:
        prompt += f"\nOrganization ID: {org.id}\n"
        if org.organization_name:
            prompt += f"Organization Name: {org.organization_name}\n"
        if org.sector_type:
            prompt += f"Sector Type: {org.sector_type}\n"
        if org.services_offered:
            prompt += f"Services Offered: {org.services_offered}\n"
        if org.city:
            prompt += f"City: {org.city}\n"
        if org.province_state:
            prompt += f"Province/State: {org.province_state}\n"
        if org.address:
            prompt += f"Address: {org.address}\n"
        if org.website:
            prompt += f"Website: {org.website}\n"
        if org.email_address:
            prompt += f"Email: {org.email_address}\n"
        if org.phone_number:
            prompt += f"Phone: {org.phone_number}\n"
        if org.contact_name:
            prompt += f"Contact Name: {org.contact_name}\n"
        if org.notes:
            prompt += f"Notes: {org.notes}\n"
        prompt += "\n"
    
    prompt += f"\n=== PROGRAMS ===\n"
    prompt += f"Total Programs Available: {len(programs)}\n\n"
    # Add all programs
    for program in programs:
        prompt += f"\nProgram ID: {program.id}\n"
        prompt += f"Title: {program.title}\n"
        if program.description:
            prompt += f"Description: {program.description}\n"
        if program.organization_id:
            # Find organization name
            org = next((o for o in organizations if o.id == program.organization_id), None)
            if org and org.organization_name:
                prompt += f"Organization: {org.organization_name}\n"
        if program.program_type:
            prompt += f"Program Type: {program.program_type}\n"
        if program.stage:
            prompt += f"Business Stage: {program.stage}\n"
        if program.sector:
            prompt += f"Sector: {program.sector}\n"
        if program.eligibility_criteria:
            prompt += f"Eligibility: {program.eligibility_criteria}\n"
        if program.cost:
            prompt += f"Cost: {program.cost}\n"
        if program.duration:
            prompt += f"Duration: {program.duration}\n"
        if program.application_deadline:
            prompt += f"Application Deadline: {program.application_deadline}\n"
        if program.start_date:
            prompt += f"Start Date: {program.start_date}\n"
        if program.website:
            prompt += f"Website: {program.website}\n"
        if program.application_link:
            prompt += f"Application Link: {program.application_link}\n"
        if program.is_verified:
            prompt += f"Verified: Yes (Innovation Zone Verified)\n"
        prompt += "\n"
    
    prompt += "\n=== EVENTS ===\n"
    # Add all events
    for event in events:
        prompt += f"\nEvent ID: {event.id}\n"
        prompt += f"Title: {event.title}\n"
        prompt += f"Description: {event.description}\n"
        prompt += f"Category: {event.category}\n"
        prompt += f"Audience: {event.audience}\n"
        prompt += f"Location: {event.location}\n"
        prompt += f"Start Date: {event.start_date}\n"
        if event.end_date:
            prompt += f"End Date: {event.end_date}\n"
        if event.link:
            prompt += f"Link: {event.link}\n"
        prompt += "\n"
    
    # Count programs for the prompt
    program_count = len(programs)
    
    prompt += f"""
=== INSTRUCTIONS ===
CRITICAL: There are {program_count} programs available in the database above. You MUST recommend at least 2-3 programs from the PROGRAMS section based on the user's responses.

1. Analyze the user's responses to all pathway questions carefully
2. You MUST match their needs with relevant PROGRAMS from the PROGRAMS section above (NOT organizations or events)
3. You MUST recommend at least 2-3 specific programs that match their responses, even if the match is not perfect
4. For each recommended program, include:
   - The exact program title as listed in the database
   - The organization offering it
   - A brief explanation of why it matches their needs
   - Eligibility requirements if available
   - How to apply (application link or website)
   - Cost, duration, and deadlines if available
5. Format your response in a clear, structured way with headings for each program
6. DO NOT say "no programs match" - you MUST find and recommend programs from the database above
7. If their responses are general, recommend the most popular or broadly applicable programs
8. DO NOT mention or recommend events - focus exclusively on PROGRAMS from the PROGRAMS section
9. Reference the exact program titles and organization names as they appear in the database

IMPORTANT: The database contains {program_count} programs. You MUST recommend programs from this list. Do not say there are no matching programs.

Your response should be helpful, personalized, and MUST include specific program recommendations from the database above.
"""
    
    return prompt


def get_gemini_response(user_responses: Dict[str, Any], pathways: List[Pathway], 
                        organizations: List[Organization], events: List[Event], programs: List[Program]) -> str:
    """Get AI response from Gemini based on user responses and database data"""
    
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in environment variables")
    
    # Check if we have programs
    if not programs or len(programs) == 0:
        return "I apologize, but there are currently no active programs available in the database. Please check back later as new programs are regularly added to the Windsor-Essex Innovation Zone Ecosystem Platform."
    
    # Build system prompt with database information
    system_prompt = build_system_prompt(pathways, organizations, events, programs)
    
    # Build user query from responses
    user_query = "Based on my responses below, please provide personalized recommendations:\n\n"
    
    # Get pathway questions and answers
    pathway_map = {p.id: p for p in pathways}
    for pathway_id, answer_key in user_responses.items():
        try:
            # Try to convert pathway_id to int, but handle string IDs too
            pathway_id_int = int(pathway_id) if isinstance(pathway_id, str) and pathway_id.isdigit() else pathway_id
            pathway = pathway_map.get(pathway_id_int)
        except (ValueError, TypeError):
            # If conversion fails, try direct lookup
            pathway = pathway_map.get(pathway_id)
        
        if pathway:
            if pathway.answer_options and isinstance(pathway.answer_options, dict):
                answer_text = pathway.answer_options.get(str(answer_key), answer_key)
            else:
                answer_text = str(answer_key)
            user_query += f"Q: {pathway.question}\nA: {answer_text}\n\n"
    
    user_query += f"\n\nIMPORTANT: There are {len(programs)} programs available in the database. You MUST recommend at least 2-3 specific programs from the PROGRAMS section that match my responses above. Include program names, descriptions, eligibility requirements, application links, and explain why each program is relevant to my needs. Do NOT say there are no matching programs - you must find and recommend programs from the database."
    
    try:
        # Initialize the model - use gemini-2.5-flash strictly
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Combine system prompt and user query
        full_prompt = f"{system_prompt}\n\n=== USER QUERY ===\n\n{user_query}"
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        # Handle response - check if text attribute exists
        if hasattr(response, 'text'):
            return response.text
        elif hasattr(response, 'candidates') and len(response.candidates) > 0:
            if hasattr(response.candidates[0], 'content'):
                if hasattr(response.candidates[0].content, 'parts'):
                    return ''.join([part.text for part in response.candidates[0].content.parts if hasattr(part, 'text')])
        else:
            return str(response)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        raise Exception(f"Error generating Gemini response: {str(e)}\n\nDetails: {error_details}")

