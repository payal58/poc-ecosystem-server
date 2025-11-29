"""Scraper for Invest WindsorEssex Foreign Trade Zone Programs"""
import os
import csv
import json
import time
import re
from datetime import datetime
from urllib.parse import urljoin

import cloudscraper
from bs4 import BeautifulSoup

BASE_URL = "https://www.investwindsoressex.com"
MAIN_URL = "https://www.investwindsoressex.com/how-we-help/incentives-and-foreign-trade-programs/foreign-trade-zone-programs/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.investwindsoressex.com/",
}


def fetch_html(url: str) -> str:
    """Fetch HTML with cloudscraper to bypass Cloudflare"""
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        raise


def extract_program_sections(soup: BeautifulSoup) -> list:
    """Extract individual program sections from the page"""
    programs = []
    
    # Find the main content area
    main_content = (
        soup.find('main') or
        soup.find('article') or
        soup.find('div', class_='entry-content') or
        soup.find('div', class_='page-content') or
        soup.body
    )
    
    if not main_content:
        return programs
    
    # Remove navigation, footer, header elements
    for element in main_content.find_all(['nav', 'footer', 'header', 'script', 'style', 'aside']):
        element.decompose()
    
    # Look for program sections - they appear to be in headings followed by paragraphs
    # Based on the content, programs are listed under "FTZ programs" section
    current_section = None
    current_description = []
    
    # Find all headings and paragraphs
    elements = main_content.find_all(['h2', 'h3', 'p', 'ul', 'li'])
    
    for element in elements:
        tag_name = element.name
        
        # Check if this is a program title (h2 or h3)
        if tag_name in ['h2', 'h3']:
            text = element.get_text(strip=True)
            
            # Check if this looks like a program name
            # Programs are: Duties Relief Program, Drawback Program, etc.
            if 'program' in text.lower() and len(text) < 100:
                # Save previous program if exists
                if current_section and current_description:
                    programs.append({
                        'title': current_section,
                        'description': ' '.join(current_description).strip()
                    })
                
                # Start new program
                current_section = text
                current_description = []
        
        # Collect description text (paragraphs, list items)
        elif tag_name in ['p', 'li'] and current_section:
            text = element.get_text(strip=True)
            # Skip very short or navigation-like text
            if len(text) > 30 and not any(noise in text.lower() for noise in [
                'contact us', 'privacy policy', 'accessibility', 'sitemap',
                'facebook', 'twitter', 'linkedin', 'instagram', 'youtube',
                'skip to content', 'language', 'search'
            ]):
                current_description.append(text)
    
    # Add last program
    if current_section and current_description:
        programs.append({
            'title': current_section,
            'description': ' '.join(current_description).strip()
        })
    
    return programs


def extract_programs_from_content(soup: BeautifulSoup) -> list:
    """Extract FTZ programs from the page content"""
    programs = []
    
    # Known program names from the page (in order they appear)
    program_names = [
        'Duties Relief Program',
        'Drawback Program',
        'Customs Bonded Warehouse Program',
        'Export Distribution Centre Program',
        'Exporters of Processing Services Program'
    ]
    
    main_content = (
        soup.find('main') or
        soup.find('article') or
        soup.find('div', class_='entry-content') or
        soup.find('div', class_='page-content') or
        soup.body
    )
    
    if not main_content:
        return programs
    
    # Remove noise
    for element in main_content.find_all(['nav', 'footer', 'header', 'script', 'style', 'aside', 'form']):
        element.decompose()
    
    # Get all text content to find program sections
    all_text = main_content.get_text(separator='\n', strip=True)
    
    # Find each program section by looking for the program name in the text
    for i, program_name in enumerate(program_names):
        # Find the position of this program name in the text
        program_idx = all_text.find(program_name)
        if program_idx == -1:
            # Try without "Program" suffix
            alt_name = program_name.replace(' Program', '')
            program_idx = all_text.find(alt_name)
            if program_idx == -1:
                continue
        
        # Find the end of this program's description (start of next program or section)
        next_program_idx = len(all_text)
        for j, next_name in enumerate(program_names[i+1:], start=i+1):
            next_idx = all_text.find(next_name, program_idx + len(program_name))
            if next_idx != -1:
                next_program_idx = next_idx
                break
        
        # Also check for section headers that might indicate end of program description
        section_markers = ['Benefits and advantages', 'Frequently asked questions', 'How We Help']
        for marker in section_markers:
            marker_idx = all_text.find(marker, program_idx + len(program_name))
            if marker_idx != -1 and marker_idx < next_program_idx:
                next_program_idx = marker_idx
                break
        
        # Extract description text for this program
        description_text = all_text[program_idx + len(program_name):next_program_idx].strip()
        
        # Clean up the description - remove extra whitespace and newlines
        description_lines = [line.strip() for line in description_text.split('\n') if line.strip()]
        # Filter out very short lines and noise
        filtered_lines = []
        for line in description_lines:
            # Skip if it's just the program name again
            if program_name.lower() in line.lower() and len(line) < len(program_name) + 20:
                continue
            # Skip navigation/footer text
            if any(noise in line.lower() for noise in [
                'contact us', 'privacy policy', 'accessibility', 'sitemap',
                'facebook', 'twitter', 'linkedin', 'instagram', 'youtube',
                'skip to content', 'language', 'search', 'main office'
            ]):
                continue
            # Skip very short lines (likely navigation)
            if len(line) > 30:
                filtered_lines.append(line)
        
        if filtered_lines:
            # Take first 3-5 meaningful paragraphs
            description = ' '.join(filtered_lines[:5])
            # Limit description length
            if len(description) > 1000:
                description = description[:1000] + '...'
            
            programs.append({
                'title': program_name,
                'description': description
            })
    
    return programs


def scrape_programs() -> list:
    """Scrape all FTZ programs from the main page"""
    print(f"Fetching: {MAIN_URL}")
    html = fetch_html(MAIN_URL)
    soup = BeautifulSoup(html, 'html.parser')
    
    # Try extracting programs
    programs = extract_programs_from_content(soup)
    
    # If we didn't find programs, try alternative method
    if not programs:
        programs = extract_program_sections(soup)
    
    # Format programs for output
    formatted_programs = []
    for program in programs:
        formatted_programs.append({
            'program_page_url': MAIN_URL,
            'program_title': program['title'],
            'program_description': program['description'],
            'application_link': MAIN_URL,  # All programs link to same page
            'program_type': 'foreign trade zone program',
            'scraped_at': datetime.utcnow().isoformat(),
        })
    
    return formatted_programs


def save_results(programs: list):
    """Save scraped programs to JSON and CSV"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, 'invest_windsor_programs.json')
    csv_file = os.path.join(script_dir, 'invest_windsor_programs.csv')
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(programs, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved JSON: {json_file}")
    
    if programs:
        fieldnames = list(programs[0].keys())
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for program in programs:
                writer.writerow(program)
        print(f"✓ Saved CSV: {csv_file}")
    
    print(f"\n✅ Scraped {len(programs)} programs")


def run():
    """Main scraping function"""
    try:
        programs = scrape_programs()
        if programs:
            save_results(programs)
        else:
            print("⚠️  No programs found")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run()
