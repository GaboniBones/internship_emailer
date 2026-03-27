import os
import requests
import json
import time
import random
from pathlib import Path

BREVO_API_KEY = os.environ["BREVO_API_KEY"]
SENDER_EMAIL = "zeberskygabriel@gmail.com"
SENDER_NAME = "Gabriel Zebersky"
CONTACTED_FILE = "C:/Users/gzebe/OneDrive/Desktop/Internships/contacted.json"

companies = [
    {
        "to": "support@govlia.com",
        "contact": "ShaKeia",
        "company": "GovLia",
        "why": "I came across GovLia while looking into Fort Lauderdale startups and the mission of helping minority-owned and veteran-owned businesses actually win government contracts is something I thought was really important. Government procurement is one of those areas where small businesses that deserve a shot often get shut out because they don't know how to navigate the system. Building a platform that changes that for founders who are already working harder than everyone else is meaningful work.",
    },
    {
        "to": "info@senzary.com",
        "contact": "Eric",
        "company": "Senzary",
        "why": "I found Senzary while looking into IoT companies in Fort Lauderdale and the AI-enabled sensor solutions for airports and industrial environments is something I wanted to learn more about. Getting real-time sensor data to actually be useful requires solving a lot of hard problems around reliability and processing and I have been trying to understand how industrial IoT systems are built. Seeing a local company doing that at a real level made me want to reach out.",
    },
    {
        "to": "info@bluefrontierac.com",
        "contact": "Daniel",
        "company": "Blue Frontier",
        "why": "I came across Blue Frontier while looking into Boca Raton cleantech companies and the liquid desiccant approach to air conditioning is something I hadn't heard of before. The idea that you can dramatically cut electricity usage from AC by storing energy as a liquid and shifting when you use power is a clever solution to a problem that really matters in Florida specifically. I'm not usually drawn to hardware startups but this one is different.",
    },
    {
        "to": "info@centah.com",
        "contact": "Gregory",
        "company": "Centah",
        "why": "I found Centah while looking into Fort Lauderdale SaaS companies and the lead and workflow management platform for home improvement retailers is something I thought was a smart niche to go after. Home improvement is a massive industry that still runs a lot of its operations on spreadsheets and phone calls. Building software that actually fits how those businesses work and helps them manage leads properly is a real problem with a big market.",
    },
    {
        "to": "customerservice@vigilantbiosciences.com",
        "contact": "Team",
        "company": "Vigilant Biosciences",
        "why": "I came across Vigilant Biosciences while looking into Fort Lauderdale healthtech companies and early detection technology for oral cancer is something that I think is really underappreciated. Most people don't get screened for oral cancer the way they get screened for other things and catching it early makes a huge difference in outcomes. Using biomarker technology to make that detection more reliable and accessible is work that actually saves lives.",
    },
    {
        "to": "communications@edisonlearning.com",
        "contact": "Team",
        "company": "EdisonLearning",
        "why": "I found EdisonLearning while looking into Fort Lauderdale edtech companies and the online K-12 education programs and blended learning solutions you provide to schools is something I have been curious about from the student side. I have been through a lot of different types of learning environments and the gap between what digital education could be and what it usually is feels pretty wide. Being around a team that is working to close that gap is something I would want to be part of.",
    },
    {
        "to": "info@premiervirtual.com",
        "contact": "Steven",
        "company": "Premier Virtual",
        "why": "I came across Premier Virtual while looking into South Florida SaaS companies and the platform for virtual job fairs and career events is something I thought was well-targeted. In-person job fairs have a lot of friction for both employers and candidates and a purpose-built platform that handles the virtual version properly is a real improvement. The fact that workforce agencies and universities are using it shows you built something that actually works.",
    },
    {
        "to": "partnerships@nationsbenefits.com",
        "contact": "Team",
        "company": "NationsBenefits",
        "why": "I found NationsBenefits while looking into Plantation FL fintech companies and the supplemental benefits management platform for health plan members is something I hadn't seen done this way before. A lot of people who have health benefits don't actually use all of them because the process is too complicated. Building software that makes those benefits more accessible and easier to use is the kind of work that has a direct impact on real people.",
    },
    {
        "to": "eddy@thefastmind.com",
        "contact": "Eddy",
        "company": "The Fastmind",
        "why": "I came across The Fastmind while looking into Plantation FL martech startups and the idea of using AI to personalize landing pages based on who clicked the ad is something I thought was genuinely clever. There is so much focus on optimizing the ad itself and almost no focus on what happens after the click. Fixing that with AI-powered personalization to match the landing experience to the specific person is a real conversion problem with a smart solution.",
    },
    {
        "to": "hello@cast.ai",
        "contact": "Team",
        "company": "Cast AI",
        "why": "I came across Cast AI while looking into Fort Lauderdale area cloud infrastructure companies and the Kubernetes cost optimization platform is something I found really interesting. Cloud costs spiraling out of control is something I have read about a lot in the context of companies trying to scale. Building an AI system that automatically right-sizes and optimizes clusters to cut costs by over 50 percent is a problem worth solving and one that touches basically every company running things on the cloud.",
    },
    {
        "to": "sales@emphasys-software.com",
        "contact": "Team",
        "company": "Emphasys Software",
        "why": "I found Emphasys while looking into Pembroke Pines software companies and the enterprise software for public housing authorities is a niche I hadn't thought about before. Government housing agencies deal with incredibly complex compliance requirements and huge amounts of data and most of them are still running on outdated systems. Building specialized software that actually fits that world and helps housing agencies run better is work that helps a lot of people who depend on public housing.",
    },
    {
        "to": "juanc.olamendy@nubisera.com",
        "contact": "Juan",
        "company": "Nubisera",
        "why": "I found Nubisera while looking into Coconut Creek tech companies and the AI-powered marketing automation for small and mid-size businesses is something I thought was well-targeted. Most AI marketing tools are built for large companies with big budgets and the SMB market often gets something either too simple or too expensive. Building tools that actually bring AI-driven marketing to smaller businesses in a practical way is a real gap you are filling.",
    },
    {
        "to": "info@ecospears.com",
        "contact": "Team",
        "company": "ecoSPEARS",
        "why": "I came across ecoSPEARS while looking into Florida environmental tech companies and the NASA-derived technology for destroying PCB and PFAS pollutants in soil and water is something I had to read about twice. PFAS contamination is one of those problems that seems huge and unsolvable and the fact that you have commercialized actual destruction technology for it rather than just containment is a big deal. This is the kind of work where science and software come together for a really concrete real-world impact.",
    },
    {
        "to": "contact@beycome.com",
        "contact": "Nico",
        "company": "Beycome",
        "why": "I came across Beycome while looking into South Florida proptech startups and the flat-fee real estate platform is something I thought was long overdue. The standard real estate commission model is one of those things everyone knows doesn't make sense anymore but nothing changes. Building an AI-powered platform that lets buyers and sellers transact for a fraction of the cost and actually getting traction with it is the kind of startup story I find interesting.",
    },
    {
        "to": "info@lumu.io",
        "contact": "Team",
        "company": "Lumu Technologies",
        "why": "I found Lumu Technologies while looking into South Florida cybersecurity companies and the real-time compromise assessment platform is something I thought was a smart approach. Most security tools tell you after something has already gone wrong. Building a continuous monitoring system that identifies breaches as they are happening rather than after the fact is a fundamentally better way to think about network security and I would want to understand how that system actually works.",
    },
]

EMAIL_TEMPLATE = """Hi {contact},

My name is Gabriel Zebersky and I'm a junior in high school from Cooper City, FL. I'm reaching out because I came across {company} and wanted to get in touch directly.

{why}

A bit about what I actually bring to the table: I've been coding in Python for a few years now and it's become my main thing. I use Claude Code for AI-assisted development and I've been building full stack web apps with a tool called Lovable. I know being 17 with no formal job experience sounds like a red flag, but I've built real projects that actually work and I learn new things really fast. I spend most of my free time on this stuff because it's what I want to do with my life and I want to get as much real experience as I can before I graduate.

What I'm really looking for is just real experience. I want to be around people who are actually building things and learn from them up close. I'm completely open to working for free, I don't need a salary right now. Even just a few hours a week remotely where I could help with something would be more valuable to me than almost anything school could teach me at this point. I can work around my schedule and I'm pretty flexible.

If there's any chance I could be useful to your team in some way I'd love to hear back. Happy to share my projects or jump on a call whenever works for you.

Thanks for taking the time to read this,
Gabriel Zebersky
zeberskygabriel@gmail.com"""


def load_contacted():
    p = Path(CONTACTED_FILE)
    if p.exists():
        with open(p) as f:
            return set(json.load(f))
    return set()


def save_contacted(contacted):
    with open(CONTACTED_FILE, "w") as f:
        json.dump(sorted(contacted), f, indent=2)


def send_email(to_email, body):
    r = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={"api-key": BREVO_API_KEY, "Content-Type": "application/json"},
        json={
            "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
            "to": [{"email": to_email}],
            "subject": "Internship Inquiry - Gabriel Zebersky | Python & AI",
            "textContent": body,
        },
    )
    return r.status_code == 201


contacted = load_contacted()
sent = 0

for c in companies:
    email = c["to"]
    if email in contacted:
        print(f"  SKIP (already contacted): {email}")
        continue

    body = EMAIL_TEMPLATE.format(
        contact=c["contact"],
        company=c["company"],
        why=c["why"],
    )

    ok = send_email(email, body)
    if ok:
        contacted.add(email)
        save_contacted(contacted)
        sent += 1
        print(f"  SENT [{sent}] -> {email}")
    else:
        print(f"  FAILED -> {email}")

    time.sleep(random.randint(20, 35))

print(f"\nDone. {sent} emails sent.")
