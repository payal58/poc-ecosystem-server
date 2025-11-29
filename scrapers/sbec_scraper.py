"""Scraper for SBEC programs"""
import os
import csv
import json
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.webusinesscentre.com"
MAIN_PATH = "/how-we-can-help/programs-and-financial-support/"
MAIN_URL = urljoin(BASE_URL, MAIN_PATH)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.webusinesscentre.com/",
}


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    normalized = urlunparse(parsed._replace(query="", fragment=""))
    return normalized.rstrip('/')


def fetch_html(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.text


def extract_description(main: BeautifulSoup) -> str:
    if not main:
        return ""

    text_blocks = []
    noise_patterns = [
        '119 chatham', 'windsor', 'contact us', 'privacy policy',
        'how we can help', 'start your business', 'grow your business',
        'news and events', 'who we are', 'office hours', 'facebook',
        'twitter', 'linkedin', 'instagram', 'language'
    ]

    elements = list(main.find_all(['p', 'li']))
    for div in main.find_all('div'):
        classes = ' '.join(div.get('class', []))
        if any(keyword in classes for keyword in ['kb-advanced-text', 'kb-accordion-text', 'kb-advanced-button-text']):
            elements.append(div)

    for element in elements:
        text = element.get_text(" ", strip=True)
        if not text:
            continue
        lower_text = text.lower()
        if any(pattern in lower_text for pattern in noise_patterns):
            continue
        # skip navigation-y short items
        if len(text.split()) < 6:
            continue
        text_blocks.append(text)

    description = ' '.join(text_blocks[:5]).strip()
    return description


def extract_first_action(main: BeautifulSoup, page_url: str) -> str:
    if not main:
        return page_url

    for link in main.find_all('a', href=True):
        text = link.get_text(" ", strip=True).lower()
        if any(keyword in text for keyword in ['apply', 'register', 'learn more', 'download', 'view guide']):
            href = link['href']
            if href.startswith('mailto:'):
                continue
            return urljoin(page_url, href)
    return page_url


def program_type_from_title(title: str) -> str:
    title_lower = (title or '').lower()
    if 'loan' in title_lower:
        return 'loan'
    if 'fund' in title_lower:
        return 'fund'
    if 'company' in title_lower or 'ventures' in title_lower:
        return 'business support'
    if 'program' in title_lower:
        return 'program'
    if 'advantage' in title_lower:
        return 'accelerator'
    return 'program'


def scrape_program(url: str) -> dict:
    html = fetch_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    main = (
        soup.find('main')
        or soup.find('div', class_='entry-content')
        or soup.find('article')
        or soup.body
        or soup
    )

    title = None
    if main and main.find('h1'):
        title = main.find('h1').get_text(strip=True)
    if not title and soup.find('h1'):
        title = soup.find('h1').get_text(strip=True)
    if not title and soup.find('title'):
        title = soup.find('title').get_text(strip=True)

    description = extract_description(main)
    application_link = extract_first_action(main, url)

    image_url = None
    if main:
        img = main.find('img')
        if img and img.get('src'):
            image_url = urljoin(url, img['src'])

    return {
        'program_page_url': url,
        'program_title': title or 'Untitled Program',
        'program_description': description,
        'application_link': application_link,
        'hero_image_url': image_url,
        'program_type': program_type_from_title(title or ''),
        'scraped_at': datetime.utcnow().isoformat(),
    }


def collect_program_links(main_html: str) -> list:
    soup = BeautifulSoup(main_html, 'html.parser')
    links = set()
    for anchor in soup.select('a[href*="/how-we-can-help/programs-and-financial-support/"]'):
        href = anchor.get('href')
        if not href:
            continue
        absolute = urljoin(BASE_URL, href)
        normalized = normalize_url(absolute)
        if normalized.rstrip('/') == normalize_url(MAIN_URL).rstrip('/'):
            continue
        links.add(normalized)
    return sorted(links)


def save_results(programs: list):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, 'sbec_programs.json')
    csv_file = os.path.join(script_dir, 'sbec_programs.csv')

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(programs, f, indent=2, ensure_ascii=False)
    fieldnames = list(programs[0].keys()) if programs else []
    if fieldnames:
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for program in programs:
                writer.writerow(program)
    print(f"✓ Saved JSON: {json_file}")
    if fieldnames:
        print(f"✓ Saved CSV: {csv_file}")


def run():
    print("Fetching SBEC Programs page...")
    main_html = fetch_html(MAIN_URL)
    program_links = collect_program_links(main_html)
    print(f"Found {len(program_links)} program links")

    programs = []
    for link in program_links:
        try:
            print(f"Scraping: {link}")
            program = scrape_program(link)
            programs.append(program)
            time.sleep(1)
        except Exception as exc:
            print(f"  ✗ Failed to scrape {link}: {exc}")
    if programs:
        save_results(programs)
    else:
        print("No programs scraped")


if __name__ == "__main__":
    run()
