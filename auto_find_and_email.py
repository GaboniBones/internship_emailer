"""
Auto Find & Email, Internship Outreach Bot
Gabriel Zebersky | zeberskygabriel@gmail.com

Scrapes the Tech Hub South Florida company directory to find tech companies,
visits their websites to find contact emails, and sends internship outreach
emails. Never emails the same company twice.
"""

import os
import re
import json
import time
import random
import logging
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# ── CONFIG ───────────────────────────────────────────────────────────────────
SENDER_EMAIL   = "zeberskygabriel@gmail.com"
SENDER_NAME    = "Gabriel Zebersky"
BREVO_API_KEY  = os.environ["BREVO_API_KEY"]

LOG_FILE               = "contacted.json"
DELAY_BETWEEN_EMAILS   = 45    # seconds between emails
MAX_EMAILS_PER_RUN     = 200   # safety cap per session
TOTAL_DIRECTORY_PAGES  = 62    # pages in the Tech Hub South FL directory
# ─────────────────────────────────────────────────────────────────────────────

EMAIL_SUBJECT = "Internship Inquiry - Gabriel Zebersky | Python & AI"

EMAIL_BODIES = [
    """\
Hi there,

My name is Gabriel Zebersky and I'm a junior in high school from Cooper City, FL. I found your company while looking into tech companies in South Florida and wanted to reach out.

I know it's a little random to get an email from a high schooler but I've been coding seriously for a few years now. I mainly work in Python and I use Claude Code for AI-assisted development. I've also been building full stack web apps with Lovable. I don't have a real job yet but I've built actual projects that work and I learn new things really quickly.

What I'm looking for is any kind of real world experience, even just a few hours a week remotely would mean a lot to me. I'm completely fine working for free. I just want to be around people who are actually building things and learn from them. School only teaches you so much and I feel like I'd grow way more from being part of a real company, even in a small way.

If there's anything at all I could help with I would really appreciate the opportunity. I'm happy to share what I've been working on or jump on a quick call if you want to talk first.

Thanks for reading,
Gabriel Zebersky
zeberskygabriel@gmail.com""",

    """\
Hi,

My name is Gabriel Zebersky. I'm 17 and a junior in high school from Cooper City, FL. I came across your company and wanted to reach out about the possibility of an internship or any kind of part time work, even unpaid.

A little about me: I've been learning to code on my own for a while and I work mainly in Python. I use Claude Code to build AI-powered projects and I've been building full stack applications with Lovable. I know I'm young and don't have a formal resume yet but I've been putting in serious time and I have real projects to show for it.

Honestly what I'm really after is experience. I want to be around people who are actually building things in tech and learn from them. I'm flexible with hours and I can work around my school schedule. I'm not asking for anything huge, even just being able to help with something small on a regular basis would be a huge deal for me.

If you think there's any chance I could be useful please let me know. I'd love to share my work or talk more about what I could help with.

Thanks,
Gabriel Zebersky
zeberskygabriel@gmail.com""",

    """\
Hey,

I hope this isn't too weird of an email to receive. My name is Gabriel Zebersky and I'm 17 years old from Cooper City, FL, currently in my junior year of high school. I've been reaching out to tech companies in South Florida because I'm really trying to get some real experience before I graduate.

Here's what I can actually do: I've been coding in Python for a while now and I've gotten pretty good at it. I've been building AI projects using Claude Code and full stack web apps with Lovable. I spend a lot of my free time on this stuff honestly. I'm not just a beginner who finished a few tutorials, I've built things that actually work and solve real problems.

I'm not expecting much. Even just helping out for a few hours a week remotely would be more than enough for me. I'll work for free, I just want to learn from people building real products. I feel like I'm at a point where I could actually contribute something useful to a small team.

If there's any chance of making something work I'd really appreciate hearing back. Happy to send over some of my projects or hop on a call.

Thanks for your time,
Gabriel Zebersky
zeberskygabriel@gmail.com""",

    """\
Hi there,

My name is Gabriel Zebersky, I'm a junior in high school from Cooper City, FL. I came across your company while researching tech companies in South Florida and decided to reach out directly.

I've been teaching myself to code for a few years and right now I work mostly in Python. I use Claude Code for AI-assisted development and I've been building full stack projects with Lovable. I've put a lot of time into this outside of school because it's what I actually want to do with my life and I want to get as much real experience as I can before I graduate.

I'm not looking for a salary or anything formal. I would genuinely work for free just to be part of something real and learn from people who know what they're doing. Even a few hours a week where I could help with a small project or task would teach me more than most things I could do at 17. I'm easy to work with and I pick things up fast.

If there's any opening at all, even something informal, I'd love to talk. Happy to share my projects or get on a call at your convenience.

Thank you,
Gabriel Zebersky
zeberskygabriel@gmail.com""",
]


# ── LOGGING SETUP ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    handlers=[
        logging.FileHandler("outreach.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


# ── CONTACT LOG ───────────────────────────────────────────────────────────────
def load_contacted() -> set:
    if Path(LOG_FILE).exists():
        with open(LOG_FILE) as f:
            return set(json.load(f))
    return set()


def save_contacted(contacted: set):
    with open(LOG_FILE, "w") as f:
        json.dump(sorted(contacted), f, indent=2)


# ── DIRECTORY SCRAPER ─────────────────────────────────────────────────────────
COMPANY_PAGE_RE = re.compile(
    r"https://techhubsouthflorida\.org/directory/[^/]+/[^/]+/$"
)


def get_company_profile_urls(page: int) -> list:
    """Fetch one page of the Tech Hub South FL directory and return company profile URLs."""
    url = (
        f"https://techhubsouthflorida.org/directory/page/{page}/"
        "?geodir_search=1&stype=gd_place&s&snear=Fort+Lauderdale"
        if page > 1
        else "https://techhubsouthflorida.org/directory/"
        "?geodir_search=1&stype=gd_place&s&snear=Fort+Lauderdale"
    )
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        seen = set()
        results = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if COMPANY_PAGE_RE.match(href) and "category" not in href and href not in seen:
                seen.add(href)
                results.append(href)
        return results
    except Exception as e:
        log.warning(f"Failed to fetch directory page {page}: {e}")
        return []


def get_company_website(profile_url: str) -> str | None:
    """Visit a Tech Hub company profile page and return the company's website URL."""
    try:
        r = requests.get(profile_url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if (
                href.startswith("http")
                and "techhubsouthflorida.org" not in href
                and "linkedin.com" not in href
                and "facebook.com" not in href
                and "twitter.com" not in href
                and "instagram.com" not in href
                and "youtube.com" not in href
            and "techhubpulse.org" not in href
            and "techhubsouthflorida.org" not in href
            ):
                return href
        return None
    except Exception as e:
        log.debug(f"Failed to fetch profile {profile_url}: {e}")
        return None


# ── EMAIL EXTRACTION ──────────────────────────────────────────────────────────
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

SKIP_DOMAINS = {
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
    "example.com", "sentry.io", "wixpress.com", "squarespace.com",
    "linkedin.com", "facebook.com", "twitter.com", "instagram.com",
    "indeed.com", "glassdoor.com", "ziprecruiter.com", "monster.com",
    "crunchbase.com", "wellfound.com", "angellist.com",
}

PREFERRED_PREFIXES = ["hello", "hi", "info", "contact", "team", "founders",
                      "jobs", "careers", "apply", "work", "intern", "hr"]


def score_email(email: str) -> int:
    local = email.split("@")[0].lower()
    for i, prefix in enumerate(PREFERRED_PREFIXES):
        if local == prefix:
            return len(PREFERRED_PREFIXES) - i
    return 0


def find_emails_on_page(url: str) -> list:
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        emails = EMAIL_RE.findall(r.text)
        filtered = []
        for e in emails:
            domain = e.split("@")[1].lower()
            if domain not in SKIP_DOMAINS and not any(s in domain for s in SKIP_DOMAINS):
                filtered.append(e.lower())
        unique = list(set(filtered))
        unique.sort(key=score_email, reverse=True)
        return unique[:5]
    except Exception:
        return []


def find_contact_email(base_url: str) -> str | None:
    """Try homepage + /contact + /about to find a contact email."""
    suffixes = ["", "/contact", "/contact-us", "/about", "/team", "/about-us"]
    for suffix in suffixes:
        url = base_url.rstrip("/") + suffix
        emails = find_emails_on_page(url)
        if emails:
            return emails[0]
        time.sleep(1)
    return None


# ── EMAIL SENDER ──────────────────────────────────────────────────────────────
def do_send(to_email: str, body: str) -> bool:
    try:
        r = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={"api-key": BREVO_API_KEY, "Content-Type": "application/json"},
            json={
                "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
                "to": [{"email": to_email}],
                "subject": EMAIL_SUBJECT,
                "textContent": body,
            },
        )
        return r.status_code == 201
    except Exception as e:
        log.error(f"Send error for {to_email}: {e}")
        return False


# ── MAIN LOOP ─────────────────────────────────────────────────────────────────
def run():
    contacted = load_contacted()
    emails_sent = 0

    log.info(f"Starting outreach bot. Already contacted: {len(contacted)} addresses.")
    log.info(f"Cap: {MAX_EMAILS_PER_RUN} emails this session.\n")

    page = 1
    while emails_sent < MAX_EMAILS_PER_RUN and page <= TOTAL_DIRECTORY_PAGES:
        log.info(f"Scraping directory page {page}/{TOTAL_DIRECTORY_PAGES}...")
        profile_urls = get_company_profile_urls(page)
        page += 1

        if not profile_urls:
            log.info("  No companies found on this page, skipping.")
            time.sleep(3)
            continue

        for profile_url in profile_urls:
            if emails_sent >= MAX_EMAILS_PER_RUN:
                break

            # Use profile URL as the dedup key for "already visited"
            if profile_url in contacted:
                log.debug(f"  Skipping {profile_url}, already visited")
                continue

            log.info(f"  Profile: {profile_url}")
            website = get_company_website(profile_url)

            if not website:
                log.info("    No website found, skipping.")
                contacted.add(profile_url)
                save_contacted(contacted)
                continue

            domain = urlparse(website).netloc.replace("www.", "")

            if domain in contacted:
                log.info(f"    Already contacted {domain}")
                contacted.add(profile_url)
                save_contacted(contacted)
                continue

            log.info(f"    Website: {website}")
            email = find_contact_email(website)

            if not email:
                log.info(f"    No email found at {domain}")
                contacted.add(profile_url)
                contacted.add(domain)
                save_contacted(contacted)
                continue

            if email in contacted:
                log.info(f"    Already contacted {email}")
                contacted.add(profile_url)
                save_contacted(contacted)
                continue

            log.info(f"    Sending to {email} ({domain})")
            success = do_send(email, random.choice(EMAIL_BODIES))

            if success:
                contacted.add(email)
                contacted.add(domain)
                contacted.add(profile_url)
                save_contacted(contacted)
                emails_sent += 1
                log.info(f"    SENT [{emails_sent}/{MAX_EMAILS_PER_RUN}] -> {email}")
                time.sleep(DELAY_BETWEEN_EMAILS + random.randint(0, 15))
            else:
                log.warning(f"    Send failed for {email}")
                time.sleep(5)

        time.sleep(random.randint(2, 5))

    if page > TOTAL_DIRECTORY_PAGES:
        log.info("Reached end of directory. All pages processed.")
    log.info(f"Session complete. {emails_sent} emails sent.")


if __name__ == "__main__":
    run()
