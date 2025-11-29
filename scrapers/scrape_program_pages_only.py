"""
Scrape only the actual program pages from WEtech Alliance
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import re
import time
from datetime import datetime
import os

class ProgramPageScraper:
    def __init__(self):
        self.base_url = "https://www.wetech-alliance.com"
        self.programs = []
        
        # Only scrape these specific program pages
        self.program_urls = [
            "https://www.wetech-alliance.com/scaleup/",
            "https://www.wetech-alliance.com/idea/",
            "https://www.wetech-alliance.com/blueprint/",
            "https://www.wetech-alliance.com/perks/",
            "https://www.wetech-alliance.com/jobs/",
            "https://www.wetech-alliance.com/wim/",
            "https://www.wetech-alliance.com/talks/",
        ]
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def extract_email(self, text):
        """Extract email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None
    
    def extract_phone(self, text):
        """Extract phone numbers from text"""
        phone_patterns = [
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
        ]
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                return phones[0]
        return None
    
    def extract_program_data(self, url, soup):
        """Extract program data from a page"""
        program = {
            'program_page_url': url,
            'program_title': None,
            'program_summary': None,
            'program_full_description': None,
            'eligibility': None,
            'target_audience': None,
            'application_deadline': None,
            'start_date': None,
            'services_offered': [],
            'contact_email': None,
            'contact_phone': None,
            'partner_organizations': [],
            'hero_image_url': None,
            'scraped_at': datetime.now().isoformat()
        }
        
        page_text = soup.get_text()
        
        # Extract title - prefer title tag, then h1, then h2
        title_tag = soup.find('title')
        if title_tag:
            title_text = title_tag.get_text().strip()
            # Clean up title (remove site name, etc.)
            if '|' in title_text:
                title_text = title_text.split('|')[0].strip()
            if ' - ' in title_text:
                title_text = title_text.split(' - ')[0].strip()
            program['program_title'] = title_text
        
        # If no good title from title tag, try h1
        if not program['program_title'] or len(program['program_title']) < 5:
            h1 = soup.find('h1')
            if h1:
                h1_text = h1.get_text().strip()
                # Skip generic headings
                if h1_text.upper() not in ['FAQ', 'IMPACT', 'UPCOMING MEETUPS', 'SUBSCRIBE TO PERSONALIZED NOTIFICATIONS', 'WETECH ALLIANCE']:
                    program['program_title'] = h1_text
        
        # Special handling for specific pages
        url_lower = url.lower()
        if '/perks/' in url_lower and (not program['program_title'] or program['program_title'].upper() == 'WETECH ALLIANCE'):
            # Look for "Client Perks" or "Regional Innovation Centre Perks" in the page
            page_text_lower = page_text.lower()
            if 'client perks' in page_text_lower:
                program['program_title'] = 'Client Perks'
            elif 'regional innovation centre perks' in page_text_lower:
                program['program_title'] = 'Regional Innovation Centre Perks'
            else:
                program['program_title'] = 'Client Perks'
        
        # If still no good title, try h2
        if not program['program_title'] or len(program['program_title']) < 5:
            h2 = soup.find('h2')
            if h2:
                program['program_title'] = h2.get_text().strip()
        
        # Extract clean program description
        # Remove all navigation, footer, header elements first
        for element in soup.find_all(['nav', 'footer', 'header', 'script', 'style', 'aside', 'form']):
            element.decompose()
        
        # Find main content - try multiple selectors
        main_content = None
        selectors = [
            ('tag', 'main'),
            ('tag', 'article'),
            ('class', 'entry-content'),
            ('class', 'page-content'),
            ('class', 'post-content'),
            ('id', 'main-content'),
        ]
        
        for selector_type, selector_value in selectors:
            try:
                if selector_type == 'tag':
                    main_content = soup.find(selector_value)
                elif selector_type == 'class':
                    main_content = soup.find(class_=selector_value)
                elif selector_type == 'id':
                    main_content = soup.find(id=selector_value)
                if main_content:
                    break
            except:
                continue
        
        if not main_content:
            main_content = soup.find('body')
        
        if main_content:
            # Remove more noise from main content
            for element in main_content.find_all(['nav', 'footer', 'header', 'script', 'style', 'aside', 'form']):
                element.decompose()
            
            # Get all text and split into sentences/paragraphs
            all_text = main_content.get_text()
            lines = [line.strip() for line in all_text.split('\n') if line.strip()]
            
            # Noise patterns to exclude
            noise_patterns = [
                '519.997.2863', '[email protected]', 'français', 'sign up', 
                'subscribe', 'contact us', 'navigation', 'home', 'who we are',
                'what we do', 'tech & innovation news', 'events', 'contact',
                'all images, designs and content copyright', 'tech it out',
                'monthly newsletter', 'get connected', 'become a client',
                'tech jobs', 'our purpose', 'our team', 'our board', 'our impact',
                'our partners', 'building community', 'connecting talent',
                'business acceleration', 'scaleup', 'i.d.e.a. fund',
                'innovation blueprint', 'client perks', 'medhealth', 'women in mobility',
                'tech talks', 'tech connect thursday', 'first robotics', 'tech awards',
                'regional alliance', 'where canada begins', 'windsor hall',
                'ferry street', 'suite 204', 'windsor, on', 'n9a 0c5',
                'mailing address', 'office:', 'connect with us'
            ]
            
            descriptions = []
            for line in lines:
                line_lower = line.lower()
                # Skip noise
                if any(noise in line_lower for noise in noise_patterns):
                    continue
                # Skip very short lines
                if len(line) < 50:
                    continue
                # Skip lines that are just menu items (few words) - but allow longer ones
                words = line.split()
                if len(words) < 8 and len(line) < 100:
                    continue
                # Skip lines that look like navigation (repeated program names in a list)
                # Check if line contains multiple program names (definitely navigation)
                program_names = ['scaleup', 'i.d.e.a. fund', 'innovation blueprint', 
                                'client perks', 'tech jobs', 'women in mobility', 
                                'tech talks', 'tech connect', 'first robotics',
                                'medhealth', 'tech awards', 'regional alliance',
                                'business acceleration', 'become a client', 'connecting talent',
                                'building community', 'get connected']
                program_name_count = sum(1 for prog in program_names if prog in line_lower)
                
                # If line contains 2+ program names, it's definitely navigation
                if program_name_count >= 2:
                    continue
                
                # If line contains program names and is short, it's likely navigation
                if program_name_count >= 1 and len(words) < 12:
                    continue
                
                # Skip lines that are just a list of program/service names
                if any(phrase in line_lower for phrase in [
                    'business acceleration', 'become a client', 'connecting talent',
                    'building community', 'get connected', 'what we do', 'who we are'
                ]) and len(words) < 20:
                    continue
                # Look for program-related content
                if any(keyword in line_lower for keyword in [
                    'program', 'provides', 'offers', 'designed', 'helps', 'supports',
                    'accelerator', 'fund', 'initiative', 'workshop', 'mentorship',
                    'entrepreneurs', 'startups', 'business', 'companies', 'clients',
                    'participants', 'applicants', 'eligibility', 'apply', 'application',
                    'cohort', 'session', 'meetup', 'workshop', 'training', 'guidance',
                    'thinking about', 'join us', 'learn about', 'discover'
                ]):
                    descriptions.append(line)
                elif len(line) > 150 and len(words) > 15:  # Long paragraphs with many words are likely descriptions
                    descriptions.append(line)
            
            if descriptions:
                # Filter out any remaining navigation-like content
                filtered_descriptions = []
                for desc in descriptions:
                    desc_lower = desc.lower()
                    # Skip if it contains multiple program names (navigation)
                    program_name_count = sum(1 for prog in program_names if prog in desc_lower)
                    if program_name_count >= 2:
                        continue
                    # Skip if it's just a list of services
                    if any(phrase in desc_lower for phrase in [
                        'business acceleration', 'become a client', 'connecting talent',
                        'building community', 'get connected'
                    ]) and len(desc.split()) < 25:
                        continue
                    filtered_descriptions.append(desc)
                
                if filtered_descriptions:
                    # Take first 3-5 meaningful descriptions
                    description_text = ' '.join(filtered_descriptions[:5])
                    # Clean up whitespace
                    description_text = ' '.join(description_text.split())
                    # Limit length
                    if len(description_text) > 2000:
                        description_text = description_text[:2000] + '...'
                    
                    program['program_full_description'] = description_text
                    program['program_summary'] = description_text[:500] if len(description_text) > 500 else description_text
                else:
                    # If all were filtered, use original descriptions but take only first one
                    if descriptions:
                        description_text = descriptions[0]
                        program['program_full_description'] = description_text[:2000]
                        program['program_summary'] = description_text[:500]
            else:
                # Last resort: get first substantial paragraph
                paragraphs = main_content.find_all('p')
                for p in paragraphs:
                    text = p.get_text().strip()
                    if len(text) > 100 and not any(noise in text.lower() for noise in noise_patterns):
                        program['program_summary'] = text[:500]
                        program['program_full_description'] = text[:2000]
                        break
        
        # Extract eligibility
        eligibility_keywords = ["eligibility", "who can apply", "target audience", "who is this for", "requirements"]
        for p in soup.find_all(['p', 'div', 'section']):
            p_text = p.get_text().lower()
            if any(keyword in p_text for keyword in eligibility_keywords):
                if 'eligibility' in p_text:
                    program['eligibility'] = p.get_text().strip()
                if 'target audience' in p_text or 'who is this for' in p_text:
                    program['target_audience'] = p.get_text().strip()
        
        # Extract services offered (bullet lists)
        for ul in soup.find_all(['ul', 'ol']):
            items = [li.get_text().strip() for li in ul.find_all('li')]
            if items and len(items) > 0:
                program['services_offered'].extend(items)
        
        # Extract contact information
        program['contact_email'] = self.extract_email(page_text)
        program['contact_phone'] = self.extract_phone(page_text)
        
        # Extract hero image
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            program['hero_image_url'] = urljoin(url, og_image['content'])
        else:
            for img in soup.find_all('img'):
                src = img.get('src') or img.get('data-src')
                if src and not any(skip in src.lower() for skip in ['icon', 'logo', 'avatar']):
                    program['hero_image_url'] = urljoin(url, src)
                    break
        
        return program
    
    def scrape(self):
        """Scrape all program pages"""
        print("Scraping WEtech Alliance program pages...\n")
        
        for url in self.program_urls:
            try:
                print(f"Scraping: {url}")
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                program = self.extract_program_data(url, soup)
                
                if program['program_title']:
                    self.programs.append(program)
                    print(f"  ✓ Found: {program['program_title']}")
                else:
                    print(f"  ⚠️  No title found for {url}")
                
                time.sleep(2)  # Be polite
                
            except Exception as e:
                print(f"  ✗ Error scraping {url}: {e}")
        
        # Save results
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(script_dir, 'wetech_programs.json')
        csv_file = os.path.join(script_dir, 'wetech_programs.csv')
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.programs, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Saved JSON: {json_file}")
        
        if self.programs:
            import csv
            fieldnames = self.programs[0].keys()
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for program in self.programs:
                    row = {}
                    for key, value in program.items():
                        if isinstance(value, list):
                            row[key] = ', '.join(value) if value else ''
                        else:
                            row[key] = value or ''
                    writer.writerow(row)
            print(f"✓ Saved CSV: {csv_file}")
        
        print(f"\n✅ Scraped {len(self.programs)} program pages")
        return self.programs

if __name__ == "__main__":
    scraper = ProgramPageScraper()
    scraper.scrape()

