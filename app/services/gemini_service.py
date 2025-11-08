"""
Gemini AI service for pathway recommendations
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Dict, List, Any
from app.models import Pathway, Organization, Event
from sqlalchemy.orm import Session

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def build_system_prompt(pathways: List[Pathway], organizations: List[Organization], events: List[Event]) -> str:
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
        prompt += f"Business Name: {org.business_name}\n"
        prompt += f"Business Stage: {org.business_stage}\n"
        prompt += f"Description: {org.description}\n"
        prompt += f"Industry: {org.industry}\n"
        if org.business_sector:
            prompt += f"Business Sector: {org.business_sector}\n"
        prompt += f"Location: {org.business_location}\n"
        prompt += f"Legal Structure: {org.legal_structure}\n"
        prompt += f"Status: {org.business_status}\n"
        if org.website:
            prompt += f"Website: {org.website}\n"
        prompt += f"Email: {org.email}\n"
        prompt += f"Phone: {org.phone_number}\n"
        if org.social_media:
            prompt += f"Social Media: {org.social_media}\n"
        if org.additional_contact_info:
            prompt += f"Additional Info: {org.additional_contact_info}\n"
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
    
    prompt += """
=== INSTRUCTIONS ===
1. Analyze the user's responses to all pathway questions
2. Match their needs with relevant organizations and events from the database
3. Provide specific, actionable recommendations
4. Reference specific organization names, event titles, and IDs when making recommendations
5. Explain why each recommendation is relevant based on their responses
6. Format your response in a clear, structured way
7. Only recommend resources that exist in the database above
8. If no good matches exist, suggest the most general relevant resources

Your response should be helpful, personalized, and based solely on the database information provided.
"""
    
    return prompt


def get_gemini_response(user_responses: Dict[str, Any], pathways: List[Pathway], 
                        organizations: List[Organization], events: List[Event]) -> str:
    """Get AI response from Gemini based on user responses and database data"""
    
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in environment variables")
    
    # Build system prompt with database information
    system_prompt = build_system_prompt(pathways, organizations, events)
    
    # Build user query from responses
    user_query = "Based on my responses below, please provide personalized recommendations:\n\n"
    
    # Get pathway questions and answers
    pathway_map = {p.id: p for p in pathways}
    for pathway_id, answer_key in user_responses.items():
        pathway = pathway_map.get(int(pathway_id))
        if pathway:
            answer_text = pathway.answer_options.get(answer_key, answer_key) if pathway.answer_options else answer_key
            user_query += f"Q: {pathway.question}\nA: {answer_text}\n\n"
    
    user_query += "\nPlease provide personalized recommendations based on my responses above."
    
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-pro')
        
        # Combine system prompt and user query
        full_prompt = f"{system_prompt}\n\n=== USER QUERY ===\n\n{user_query}"
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        return response.text
    except Exception as e:
        raise Exception(f"Error generating Gemini response: {str(e)}")

