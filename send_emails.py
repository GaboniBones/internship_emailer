"""
Internship Cold Email Sender
Gabriel Zebersky | zeberskygabriel@gmail.com

SETUP (required before running):
1. Go to brevo.com and create a free account
2. Go to Settings -> SMTP & API -> copy your SMTP Key
3. Paste it into BREVO_SMTP_KEY below
"""

import os
import requests

# ── CONFIG ──────────────────────────────────────────────────────────────────
SENDER_EMAIL   = "zeberskygabriel@gmail.com"
SENDER_NAME    = "Gabriel Zebersky"
BREVO_API_KEY  = os.environ["BREVO_API_KEY"]
# ────────────────────────────────────────────────────────────────────────────

companies = [
    # ── BROWARD COUNTY / SOUTH FLORIDA ──────────────────────────────────────
    {
        "to": "hello@lamatic.ai",
        "company": "Lamatic.ai",
        "contact": "Charles",
        "why": "I came across Lamatic.ai while going down a rabbit hole on AI companies in South Florida and the concept clicked with me right away. Helping small businesses actually plug into AI without needing to build out their own infrastructure is a problem that not enough people are focused on. I thought the way you approached it was smart and it's something I've been thinking about a lot in my own projects too.",
        "role_fit": "AI/ML and Python development",
    },
    {
        "to": "info@authorityai.ai",
        "company": "Authority AI",
        "contact": "Allen",
        "why": "I found Authority AI while looking into Fort Lauderdale's AI scene and the focus on bringing real automation to small businesses caught my attention right away. AI automation is where I've been putting most of my own learning time lately, so seeing a local company doing it at a real level made me want to reach out.",
        "role_fit": "AI automation and Python scripting",
    },
    {
        "to": "support@aracor.ai",
        "company": "Aracor AI",
        "contact": "Team",
        "why": "I came across Aracor while looking up AI startups in South Florida and the idea of using AI for deal analysis is not something I had seen tackled this way before. It's a really specific problem and I liked that you went after something hard and niche instead of building another generic AI product. That kind of focus is something I genuinely respect.",
        "role_fit": "AI/ML and Python development",
    },
    {
        "to": "info@helixvm.com",
        "company": "HelixVM",
        "contact": "Robert",
        "why": "I found HelixVM while looking at telehealth companies in South Florida and the way you're making virtual care actually accessible is something that stood out to me. I have family members who have used telehealth and the difference between a good and bad platform is huge. The fact that you're focused on making that experience better for patients is something I think matters a lot.",
        "role_fit": "Python development and data analysis",
    },
    {
        "to": "support@xendoo.com",
        "company": "Xendoo",
        "contact": "Lil",
        "why": "I came across Xendoo while looking into fintech companies in Fort Lauderdale and the focus on cloud bookkeeping for small businesses is something that makes a lot of sense to me. My parents run a small business and the accounting side is always a headache. Seeing a company that built a real software solution for that problem and actually got it to work at scale is something I find impressive.",
        "role_fit": "Python development and data analytics",
    },
    {
        "to": "info@carepredict.com",
        "company": "CarePredict",
        "contact": "Satish",
        "why": "I found CarePredict while looking into healthtech companies in Broward County and the work you're doing with AI to predict care needs for seniors is something I really connected with. I have grandparents and the idea of technology being able to catch problems early and keep them safer feels very real to me. It's not just a cool tech application, it actually helps people.",
        "role_fit": "AI/ML and Python development",
    },
    {
        "to": "info@cloudhesive.com",
        "company": "CloudHesive",
        "contact": "James",
        "why": "I came across CloudHesive while looking into Fort Lauderdale tech companies and the specialization in cloud security and AWS work caught my eye. I've been learning about cloud infrastructure on my own but there's a limit to what you can figure out from tutorials. Being around a team that does this work every day for real clients is exactly the kind of environment where I'd actually learn it properly.",
        "role_fit": "Cloud infrastructure and Python automation",
    },
    {
        "to": "info@boatyard.com",
        "company": "Boatyard",
        "contact": "Team",
        "why": "I found Boatyard while looking into Fort Lauderdale startups and the problem you're solving is one I've actually seen up close. Growing up in South Florida you see a lot of boats and you also see how disorganized the whole service and maintenance side can be. Building a platform that actually brings that online in a way that works is a real problem worth solving.",
        "role_fit": "Software development and mobile apps",
    },
    {
        "to": "info@rocked.us",
        "company": "The RockED Company",
        "contact": "Team",
        "why": "I came across The RockED Company while looking into Fort Lauderdale startups and the idea of breaking learning down into short focused content for sales teams is something I thought was smart. Most training content is too long and people zone out. The micro-learning format makes a lot of sense and I've seen it work with the way I learn things too.",
        "role_fit": "Software development and edtech",
    },
    {
        "to": "support@highrewardsapp.com",
        "company": "HighRewards",
        "contact": "Josh",
        "why": "I found HighRewards while looking into AI-powered apps in Fort Lauderdale and the concept of using AI to make loyalty rewards actually feel worth it is something I thought was a clever angle. Most rewards apps are pretty boring and people stop using them quickly. Using AI to make it feel more engaging is a real solution to a real problem.",
        "role_fit": "AI/ML and Python development",
    },
    {
        "to": "start@apolo.us",
        "company": "Apolo",
        "contact": "Bill",
        "why": "I came across Apolo while looking into AI infrastructure companies in Fort Lauderdale and the focus on private AI cloud is something I think is really important right now. A lot of companies want to use AI but can't just send their data to a third party. Building the infrastructure that lets them run it privately and securely is a hard problem and I think it's going to matter more and more.",
        "role_fit": "AI infrastructure and Python development",
    },
    {
        "to": "info@subbase.io",
        "company": "SubBase",
        "contact": "Eric",
        "why": "I found SubBase while looking into Broward County tech companies and the problem you're solving in construction is something I hadn't thought much about before. Once I read into it I realized how much of materials procurement is still done manually and on spreadsheets. Building software to fix that for an industry that really needs it is the kind of practical problem I like thinking about.",
        "role_fit": "SaaS development and Python",
    },
    {
        "to": "info@mybundle.tv",
        "company": "MyBundle.TV",
        "contact": "Jason",
        "why": "I came across MyBundle.TV while looking into Fort Lauderdale startups and the streaming bundle problem is literally something my family deals with constantly. We have like four different subscriptions and nobody can figure out what's on which service. The fact that you built a platform that helps people and ISPs deal with that confusion is something I relate to on a personal level.",
        "role_fit": "Software engineering and data analytics",
    },
    {
        "to": "info@myvert.com",
        "company": "VERT",
        "contact": "Martin",
        "why": "I found VERT while looking into sports tech companies in Fort Lauderdale and the wearable jump measurement technology stood out to me. I've played sports my whole life and the amount of guesswork that goes into training is a real issue. Having actual data from a wearable that coaches and athletes can act on is something I can see making a real difference.",
        "role_fit": "Data analytics and Python development",
    },
    {
        "to": "info@ubicquia.com",
        "company": "Ubicquia",
        "contact": "Ian",
        "why": "I came across Ubicquia while looking into IoT companies in Fort Lauderdale and using streetlights as the base layer for smart city infrastructure is honestly one of the most clever ideas I've seen. The hardware is already everywhere, it already has power and connectivity, and you turn it into something way more useful. That kind of thinking about problems is something I really want to learn from.",
        "role_fit": "IoT and data engineering",
    },
    {
        "to": "contact@payallps.com",
        "company": "Payall Payment Systems",
        "contact": "Gary",
        "why": "I found Payall while looking into fintech companies in Fort Lauderdale and the focus on cross-border payment infrastructure is something I've been curious about. The fact that moving money internationally is still so slow and expensive when data moves instantly is something I've never fully understood. Building payment rails that actually fix that at the institutional level seems like really important work.",
        "role_fit": "Software engineering and fintech",
    },
    {
        "to": "jobs@energyx.com",
        "company": "EnergyX",
        "contact": "Team",
        "why": "I came across EnergyX while looking into Fort Lauderdale's tech ecosystem and lithium extraction technology is not something I expected to find locally. The bottleneck on battery technology being lithium supply is something I've read a lot about and the idea that you're working on extraction technology that could actually change that supply chain is a big deal. I'm not usually drawn to hardware companies but this one got my attention.",
        "role_fit": "Data analysis and Python development",
    },
    {
        "to": "info@gobodhi.com",
        "company": "Bodhi",
        "contact": "Will",
        "why": "I found Bodhi while looking at Fort Lauderdale startups and building management software is something I hadn't thought much about until I read into what you're doing. The amount of energy and resources that get wasted in commercial buildings because of bad systems is a real problem. Using software to actually optimize that is both a business opportunity and something that matters for other reasons too.",
        "role_fit": "Software development and IoT",
    },
    {
        "to": "info@piere.com",
        "company": "Piere",
        "contact": "Yuval",
        "why": "I came across Piere while looking into fintech startups in Fort Lauderdale and the idea of a personalized budget planner that actually adapts to how you spend is something I wish existed more. I'm at an age where I'm starting to think about money seriously and most budgeting tools feel either too basic or too complicated. What you're building sounds like it could actually be useful to real people.",
        "role_fit": "Python development and data analytics",
    },
    {
        "to": "info@shipmonk.com",
        "company": "ShipMonk",
        "contact": "Team",
        "why": "I found ShipMonk while looking into Fort Lauderdale's bigger tech companies and the growth you've had is honestly impressive. Managing fulfillment for thousands of e-commerce brands at once requires really complex logistics software and I'd love to understand how systems like that are actually built. The scale of what you're running is the kind of engineering challenge I want to learn about.",
        "role_fit": "Software engineering and data analytics",
    },
    {
        "to": "contact@boatsetter.com",
        "company": "Boatsetter",
        "contact": "Michael",
        "why": "I came across Boatsetter while looking into Fort Lauderdale startups and honestly growing up in South Florida you hear about boat rentals all the time. Building a marketplace that actually makes that work, handles the trust and insurance side and gets real traction, is something a lot of people tried and couldn't pull off. The fact that you became the biggest one is something worth learning from.",
        "role_fit": "Software engineering and marketplace analytics",
    },
    {
        "to": "info@qolo.io",
        "company": "Qolo",
        "contact": "Patricia",
        "why": "I found Qolo while looking into Fort Lauderdale fintech companies and the programmable payments platform caught my attention right away. The ability for companies to issue cards and move money programmatically is something I've run into as a concept when building projects. Understanding how to build that infrastructure at a real level is something I'd really want to learn.",
        "role_fit": "Software engineering and fintech",
    },
    {
        "to": "info@fitmatch.ai",
        "company": "FIT:MATCH",
        "contact": "Haniff",
        "why": "I came across FIT:MATCH while looking into AI companies in Fort Lauderdale and the 3D body scanning technology for clothing fit is something I hadn't seen done this way before. The fit problem in online retail seems simple but is actually really hard to solve and the computer vision approach seems like the right way to do it. It's a practical application of AI that solves a real consumer problem.",
        "role_fit": "AI/ML and Python development",
    },
    {
        "to": "peter@athliance.co",
        "company": "Athliance",
        "contact": "Peter",
        "why": "I found Athliance while looking into Fort Lauderdale startups and the NIL space is something I've been following closely since it opened up. The amount of confusion and risk for student athletes trying to figure out what they can and can't do is a real problem. Building a platform that helps them navigate that and actually benefit from their name and image safely is work that matters to a lot of people.",
        "role_fit": "Software engineering and compliance tech",
    },
    {
        "to": "info@sellersfi.com",
        "company": "SellersFi",
        "contact": "Ricardo",
        "why": "I came across SellersFi while looking into Weston tech companies and the e-commerce financing model is something I thought was really clever. A lot of small online sellers have the demand and the products but can't grow because of cash flow gaps in inventory. Building a fintech product specifically designed to fix that for e-commerce businesses makes a lot of sense to me.",
        "role_fit": "Data analytics and Python development",
    },
    {
        "to": "info@proathletecommunity.com",
        "company": "Pro Athlete Community",
        "contact": "Team",
        "why": "I found Pro Athlete Community while looking into Fort Lauderdale startups and the concept of using professional athletes as the network for executive mentorship is something I hadn't seen before. Athletes have been through extreme high-pressure situations and the lessons from that translate to business in ways that normal coaching can't replicate. It's a smart and original idea.",
        "role_fit": "Software development and data analytics",
    },
    {
        "to": "info@travel.win",
        "company": "travel.win",
        "contact": "Team",
        "why": "I came across travel.win while looking into Fort Lauderdale's funded startups and travel planning is still way harder than it should be. Every time I've tried to plan a trip with friends or family there are like ten different tools involved and nothing talks to each other. Whatever you're building to fix that is something I'm curious about.",
        "role_fit": "Software engineering and AI",
    },
    {
        "to": "info@zulupods.com",
        "company": "Zulu Pods",
        "contact": "Team",
        "why": "I found Zulu Pods while looking into Fort Lauderdale defense and aerospace companies and the dual-use fluid delivery technology is something I wanted to understand better. Building something engineered to defense standards and then finding commercial applications for it is a smart approach. I don't know a ton about this space yet but that's exactly why I want to learn.",
        "role_fit": "Engineering and data analysis",
    },
    {
        "to": "info@magicleap.com",
        "company": "Magic Leap",
        "contact": "Team",
        "why": "I've been following Magic Leap for years honestly. The idea of AR that actually works in a real enterprise setting and helps people do their jobs better is something I've been curious about for a long time. The shift toward practical enterprise use cases feels like the right direction and I'd really want to understand how that software actually gets built and iterated on.",
        "role_fit": "Software engineering and AI/ML",
    },
    {
        "to": "info@hotwirecommunications.com",
        "company": "Hotwire Communications",
        "contact": "Team",
        "why": "I found Hotwire Communications while researching Fort Lauderdale tech companies and the fiber-optic network build-out is something I think matters more than people realize. Fast reliable internet access changes what's possible for whole communities and building that infrastructure locally is real work with real impact. I grew up on Hotwire internet actually so this one hit a little different for me.",
        "role_fit": "Network engineering and software development",
    },
    {
        "to": "info@ibusinessfunding.com",
        "company": "iBusiness Funding",
        "contact": "Team",
        "why": "I came across iBusiness Funding while looking into Fort Lauderdale fintech companies and the focus on automating small business lending is something I think is really needed. Traditional bank loan processes for small businesses are painfully slow and a lot of businesses that should get funded don't because of all the friction. Building software that cuts through that and gets capital to businesses faster is work with real consequences.",
        "role_fit": "Python development and fintech analytics",
    },
    {
        "to": "info@modmed.com",
        "company": "Modernizing Medicine",
        "contact": "Team",
        "why": "I came across Modernizing Medicine while looking into South Florida healthtech companies and the work you've done on EHR systems for specialty practices is something I had to read more about. Most EHR software has a reputation for being terrible to use and building something specialty-specific that doctors actually like is a real achievement. The connection between better software and better patient outcomes is something I care about.",
        "role_fit": "Software engineering and healthcare data",
    },
    {
        "to": "info@afgsim.com",
        "company": "Avenger Flight Group",
        "contact": "Team",
        "why": "I found Avenger Flight Group while looking into Fort Lauderdale tech companies and flight simulation software is something I was immediately curious about. Getting pilot training right matters in a direct way because the consequences of bad training are serious. Building simulation software accurate enough to actually prepare pilots is a technical challenge I'd really want to understand better from the inside.",
        "role_fit": "Software engineering and simulation",
    },
    {
        "to": "media@syncromune.com",
        "company": "Syncromune",
        "contact": "Eamonn",
        "why": "I came across Syncromune while looking into Fort Lauderdale biotech companies and personalized cancer immunotherapy is something I've been reading about a lot lately. The idea that your immune system can be trained to fight cancer specifically is something that could change everything about how cancer gets treated. I know the data and software side is where I could actually contribute and this is a mission I'd be proud to work toward.",
        "role_fit": "Data analysis and bioinformatics",
    },
    # ── BROWARD TECH / SOFTWARE ENGINEERING ──────────────────────────────────
    {
        "to": "info@ukg.com",
        "company": "UKG (Ultimate Kronos Group)",
        "contact": "Team",
        "why": "I came across UKG while looking into Weston tech companies and the scale of what you've built is something I had to wrap my head around. Workforce management software for hundreds of thousands of organizations touches basically every employee action at companies across the country. The engineering complexity behind something that has to work that reliably at that scale is exactly the kind of thing I want to learn about from people who actually built it.",
        "role_fit": "Software engineering and data analytics",
    },
    {
        "to": "techcareers@chewy.com",
        "company": "Chewy",
        "contact": "Team",
        "why": "I came across Chewy's engineering presence in Dania Beach while looking into Broward County tech companies and I honestly didn't know how much of Chewy's technical operation was run from here. The backend systems behind a platform that ships pet supplies to millions of households and handles all the logistics and customer service tech is a really complex engineering problem. Being around that kind of scale would teach me things I couldn't learn anywhere else.",
        "role_fit": "Software engineering and backend development",
    },
    {
        "to": "info@citrix.com",
        "company": "Citrix",
        "contact": "Team",
        "why": "I came across Citrix while looking into Fort Lauderdale tech companies and the work in cloud computing and virtualization is something I've bumped into a lot without fully understanding how it works under the hood. The products you build let millions of people access work systems from anywhere securely and figuring out how to make that actually work reliably at scale is a problem I'd really want to dig into.",
        "role_fit": "Software engineering and cloud infrastructure",
    },
    {
        "to": "info@bluestreamhealth.com",
        "company": "Bluestream Health",
        "contact": "Team",
        "why": "I found Bluestream Health while looking at telehealth companies in Fort Lauderdale and the white-label virtual care platform approach is something I thought was smart. Health systems want to offer telehealth but they don't all have the resources to build it from scratch. Building something reliable enough that hospitals will stake their patient relationships on it is a genuinely hard problem.",
        "role_fit": "Python development and healthcare software",
    },
    {
        "to": "info@openkey.co",
        "company": "OpenKey",
        "contact": "Team",
        "why": "I came across OpenKey while looking into Fort Lauderdale startups and the mobile hotel key problem is something I've thought about every time I've been in a hotel and had to go back to the front desk for a new key card. The fact that this is still how hotels handle it is kind of wild. Getting the mobile experience right while working with the hardware integrations that hotels already have is a real engineering challenge.",
        "role_fit": "Mobile and backend software development",
    },
    {
        "to": "info@cyberfortress.com",
        "company": "Cyber Fortress",
        "contact": "Team",
        "why": "I found Cyber Fortress while looking into cybersecurity companies in Broward County and the focus on protecting small and mid-sized businesses is something I think is really needed. Most SMBs don't have a security team and they're easy targets. Building products that give them real protection without requiring them to hire experts is solving a problem that matters to a lot of businesses.",
        "role_fit": "Cybersecurity and Python development",
    },
    {
        "to": "info@datalink.com",
        "company": "Datalink Networks",
        "contact": "Team",
        "why": "I came across Datalink Networks while looking into Broward County IT infrastructure companies and the breadth of work across cloud, security, and managed services is something I'd want to understand better. I've been learning cloud stuff on my own but there's a big gap between what you pick up from documentation and what you learn from actually working on real enterprise infrastructure.",
        "role_fit": "Cloud infrastructure and software engineering",
    },
    {
        "to": "contact@solarwinds.com",
        "company": "SolarWinds",
        "contact": "Team",
        "why": "I came across SolarWinds while looking into Broward County tech companies and the observability and IT management tools you build are something I've read about in the context of understanding how large systems are monitored. Writing software that gives engineers visibility into complex infrastructure is a problem I find really interesting and learning how that works from people who build it professionally would be a big deal for me.",
        "role_fit": "Software engineering and systems monitoring",
    },
    {
        "to": "info@carpedata.com",
        "company": "Carpe Data",
        "contact": "Team",
        "why": "I found Carpe Data while looking into Fort Lauderdale insurtech companies and the alternative data approach to insurance underwriting is something I thought was really interesting. The idea that there's information from online sources that can make underwriting more accurate than traditional methods is a problem where machine learning actually makes sense. I've been learning ML and seeing it applied to a real business problem with measurable results is something I'd want to be part of.",
        "role_fit": "Data engineering and AI/ML development",
    },
    # ── BROWARD BUSINESS MARKETING COMPANIES ────────────────────────────────
    {
        "to": "hello@tandem.buzz",
        "company": "Tandem Interactive",
        "contact": "Team",
        "why": "I came across Tandem Interactive while looking into Fort Lauderdale marketing agencies and the range of clients you work with from local businesses to Fortune 500 companies is impressive. The fact that you've built an agency that can serve both ends of that spectrum means you're doing something right. I'd want to learn how digital strategy and execution actually works from a team that does it at that level.",
        "role_fit": "digital marketing, SEO, and data-driven campaign support",
    },
    {
        "to": "info@savageglobalmarketing.com",
        "company": "Savage Global Marketing",
        "contact": "Team",
        "why": "I found Savage Global Marketing while looking into Fort Lauderdale agencies and the boutique approach to branding caught my attention. There's a real difference between an agency that just runs ads and one that actually thinks about how a brand tells its story. The combination of creative work and digital strategy is something I'd want to learn more about and understand how it comes together in practice.",
        "role_fit": "creative marketing, branding, and social media",
    },
    {
        "to": "info@docdigitalsem.com",
        "company": "Doc Digital SEM",
        "contact": "Team",
        "why": "I came across Doc Digital SEM while looking into local Fort Lauderdale agencies and the specialization in search marketing and lead generation is something I've been trying to learn more about. The data side of SEO and SEM connects well with the Python and analytics work I've been doing on my own. I'd want to understand how search strategy actually gets built and measured by people who do it professionally.",
        "role_fit": "SEO, SEM, and digital analytics",
    },
    {
        "to": "jc@hashtagdigitalmarketing.com",
        "company": "Hashtag Digital Marketing Group",
        "contact": "JC",
        "why": "I found Hashtag Digital Marketing while looking into Pembroke Pines agencies and the focus on helping local South Florida businesses is something I liked about your approach. I'm from Cooper City so seeing a South Florida company specifically focused on growing businesses in this area is something I connect with. Being part of a small team where I can actually see how things work and contribute in a real way is exactly what I'm looking for.",
        "role_fit": "social media marketing, SEO, and web support",
    },
    {
        "to": "info@marketingcartel.com",
        "company": "The Marketing Cartel",
        "contact": "Team",
        "why": "I came across The Marketing Cartel while looking into Coral Springs agencies and the focus on measurable results from SEO and paid search is something that appeals to me. I like that you can actually track whether what you're doing is working. The analytical side of digital marketing is something I want to understand better and being around a team focused on real results would help me learn that.",
        "role_fit": "SEO, Google Ads, and lead generation",
    },
    {
        "to": "sales@cfsearchmarketing.com",
        "company": "CF Search Marketing",
        "contact": "Team",
        "why": "I found CF Search Marketing while looking into Broward County agencies and the data-driven approach to search marketing is something I connected with my own work. I spend a lot of time thinking about how to measure things and find patterns in data through Python. The same kind of analytical thinking seems to apply to understanding why certain keywords and campaigns work and others don't and I'd want to learn that side of it properly.",
        "role_fit": "SEO, PPC, and paid search analytics",
    },
    {
        "to": "info@ringomedia.com",
        "company": "Ringo Media",
        "contact": "Team",
        "why": "I came across Ringo Media while looking into Fort Lauderdale agencies and the combination of marketing services and software solutions is something that stood out. Most agencies do one or the other. The fact that you do both means you can build things as well as market them and that's the kind of environment where I could apply both sides of what I've been learning.",
        "role_fit": "web development, SEO, and digital marketing",
    },
    {
        "to": "info@sociallybuzz.com",
        "company": "Sociallybuzz",
        "contact": "Team",
        "why": "I found Sociallybuzz while looking into Weston marketing agencies and the reputation you've built in social media advertising and reputation management stood out to me. Being from South Florida and seeing a local agency win real recognition in the digital marketing space is something I respect. I'd want to learn from a team that has figured out what actually works in social.",
        "role_fit": "social media marketing, paid ads, and content strategy",
    },
    {
        "to": "contact@blueinteractiveagency.com",
        "company": "Blue Interactive Agency",
        "contact": "Team",
        "why": "I came across Blue Interactive Agency while looking into Fort Lauderdale marketing firms and seeing that you have a formal internship program is something that stood out to me. It tells me you actually invest time in helping younger people learn, which is exactly what I'm looking for. The full-service approach across SEO, PPC, and content is the kind of environment where I'd be exposed to all the different pieces and understand how they fit together.",
        "role_fit": "SEO, PPC, content marketing, and web support",
    },
    {
        "to": "hello@dazos.com",
        "company": "Dazos",
        "contact": "David",
        "why": "I came across Dazos while looking into South Florida healthtech companies and a CRM built specifically for behavioral health providers is something I thought was really specific in a good way. Mental health treatment has unique operational challenges that generic CRM software doesn't address at all. Building something purpose-built for that space where the stakes for patients are high is work I'd be glad to be part of.",
        "role_fit": "Data analytics and software development",
    },
    {
        "to": "info@beesion.com",
        "company": "Beesion",
        "contact": "Omar",
        "why": "I found Beesion while looking into Fort Lauderdale software companies and the low-code approach for telecom companies operating across 20 countries is something I had to read more about. Telecom backend systems are notoriously complex and building a platform that lets them configure workflows without custom code at that scale is a hard problem. The global reach you've built is something I wouldn't have expected to find based in Fort Lauderdale.",
        "role_fit": "Software development and Python",
    },
    {
        "to": "info@datacore.com",
        "company": "DataCore Software",
        "contact": "Dave",
        "why": "I came across DataCore while looking into Fort Lauderdale software companies and software-defined storage is something I've been trying to understand better. The gap between storing data and managing it efficiently at enterprise scale is a lot bigger than I initially thought. Being around a team that has been solving that problem for a long time and building products that enterprises actually depend on would be really valuable.",
        "role_fit": "Software engineering and data infrastructure",
    },
    {
        "to": "info@catalystgem.com",
        "company": "Catalyst GEM",
        "contact": "John",
        "why": "I found Catalyst GEM while looking into Fort Lauderdale edtech companies and the focus on international student admissions at scale is something I found interesting. Getting into a school in another country involves a lot of moving parts and most of it is still done manually. Building software that makes that process work for both students and institutions is a real problem worth solving.",
        "role_fit": "Software development and data analytics",
    },
    {
        "to": "info@classwallet.com",
        "company": "ClassWallet",
        "contact": "Jamie",
        "why": "I came across ClassWallet while looking into South Florida edtech companies and the numbers involved made me look twice. Moving over 2.7 billion dollars in public funds to teachers and schools across 32 states is not a small thing. Building the software infrastructure to handle that correctly and compliantly is a real fintech challenge and one where getting it right actually matters for a lot of kids and teachers.",
        "role_fit": "Software engineering and fintech",
    },
    {
        "to": "info@synthbee.com",
        "company": "SynthBee",
        "contact": "Rony",
        "why": "I came across SynthBee while looking into Fort Lauderdale AI startups and the mission of using AI to take ideas from concept to manufacturing faster is something I found really ambitious. The fact that the founder also started Magic Leap made me look into this more carefully. Applying AI to compress the product development cycle for enterprises is a problem that could change how new things get built and I'd really want to be around that work.",
        "role_fit": "AI development and Python",
    },
    {
        "to": "info@sandbx.co",
        "company": "SANDBX",
        "contact": "Uri",
        "why": "I found SANDBX while looking into Fort Lauderdale software development companies and the variety of products you've shipped is something that caught my attention. Working across different industries means you're always solving new problems in new contexts. Building that kind of adaptability early on is something I think is really valuable and I'd want to be part of a team that actually ships things.",
        "role_fit": "Software development and Python",
    },
    {
        "to": "info@gogig.com",
        "company": "GoGig",
        "contact": "Chris",
        "why": "I came across GoGig while looking into Fort Lauderdale startups and the anonymous professional networking approach is something I thought was clever. Most job platforms feel like you're just throwing a resume into a void. The idea of matching people based on who they actually are and what they want, before revealing identities, changes the whole dynamic of how that conversation starts.",
        "role_fit": "Software engineering and AI/ML",
    },
    {
        "to": "Heroes@CaptainCompliance.com",
        "company": "Captain Compliance",
        "contact": "Richart",
        "why": "I came across Captain Compliance after reading about the Venture Atlanta win and growing over 1000% in a single year is something I wanted to understand better. Privacy and data compliance is an area that more businesses are taking seriously and building software that actually helps them get there is the kind of practical product that fills a real gap. I'd want to learn from a team that built something that fast.",
        "role_fit": "Software development and compliance tech",
    },
    {
        "to": "info@chetu.com",
        "company": "Chetu",
        "contact": "Atal",
        "why": "I came across Chetu while looking into Fort Lauderdale software companies and the scale of the operation with over 2800 engineers is something that's hard to wrap your head around. Shipping software solutions across that many industries at once requires systems and processes that I'd really want to understand. I know being around a team that big and productive would teach me things you can't learn from building projects on your own.",
        "role_fit": "Software development and Python",
    },
    {
        "to": "info@alkemy.org",
        "company": "Alkemy",
        "contact": "Jonathan",
        "why": "I found Alkemy while looking into Coral Springs tech companies and handling everything from web design to development to digital strategy in one place is an approach that interests me. I've been learning different parts of building things separately and seeing how they all connect in a real agency setting is something I'd learn a lot from. Being around people who own the whole lifecycle is exactly what I'm looking for right now.",
        "role_fit": "Web development and software engineering",
    },
    {
        "to": "dpizzo@itsolutions247.com",
        "company": "IT Solutions of South Florida",
        "contact": "Deana",
        "why": "I came across IT Solutions of South Florida while looking into Broward cybersecurity companies and the 21-year track record you've built is something you don't see very often in tech. Managed services and cybersecurity require a level of trust that takes a long time to earn and the fact that you've maintained that for over two decades locally means you're doing something right. I'd want to learn from a team with that kind of experience.",
        "role_fit": "Cybersecurity and IT support",
    },
    {
        "to": "info@flagler.io",
        "company": "Flagler Technologies",
        "contact": "Laura",
        "why": "I found Flagler Technologies while looking into South Florida IT companies and the range of services you provide to businesses across the region is something I'd want to get exposure to. Understanding how businesses actually set up and maintain their technology infrastructure is something you can only really learn by being around it. I want to understand the full picture of how companies build and manage their IT, not just the software development side.",
        "role_fit": "IT solutions and software development",
    },
    {
        "to": "info@mybambu.com",
        "company": "MyBambu",
        "contact": "Doug",
        "why": "I came across MyBambu while looking into South Florida fintech companies and the focus on mobile banking for underserved Latino communities is something I found really meaningful. Growing up in South Florida you see how many people don't have access to basic banking services and the real costs that come with that. Building a product that changes that for a community this large is the kind of work I'd be proud to help with in any way I could.",
        "role_fit": "Software engineering and fintech",
    },
    {
        "to": "jeff@bocatech.com",
        "company": "Boca Tech and Automation",
        "contact": "Jeff",
        "why": "I found Boca Tech and Automation while looking into South Florida smart home companies and the hands-on work of building automation systems that actually work in people's homes sounds like a really different kind of technical challenge. Getting hardware, software, and networking to all work together reliably in a real environment requires different problem solving than pure software development and I'd want to understand that.",
        "role_fit": "Software development and IoT automation",
    },
    {
        "to": "info@technearshore.com",
        "company": "TechNearshore",
        "contact": "Jim",
        "why": "I came across TechNearshore while looking into Boca Raton software companies and the focus on enterprise software development for global brands is something I wanted to learn more about. There's a big difference between the projects I build on my own and what goes into enterprise software at a real scale. Working alongside engineers who do that kind of work every day would teach me things I couldn't get anywhere else at my stage.",
        "role_fit": "Software development and Python engineering",
    },
    {
        "to": "liviu@zerobounce.net",
        "company": "ZeroBounce",
        "contact": "Liviu",
        "why": "I came across ZeroBounce while looking into Boca Raton SaaS companies and the scale of what you've built is something I actually read twice. Processing billions of email verifications for over 350,000 customers is a data infrastructure problem that requires a level of reliability and performance I'd really want to understand. Building and running something at that scale from Boca Raton is genuinely impressive.",
        "role_fit": "Python development and data engineering",
    },
    {
        "to": "info@mobilehelp.com",
        "company": "MobileHelp",
        "contact": "Team",
        "why": "I found MobileHelp while looking into Boca Raton healthtech companies and the connected medical alert products are something my family has actually talked about for older relatives. The software behind something that has to be reliable enough to work in an emergency is a different kind of challenge than most products. Getting the IoT hardware, cloud connectivity, and real-time response all working correctly in a life-critical context is work I'd take seriously.",
        "role_fit": "Software development and IoT",
    },
    {
        "to": "info@fortegrp.com",
        "company": "Forte Group",
        "contact": "Team",
        "why": "I came across Forte Group while looking into Boca Raton software firms and the focus on enterprise application development and modernization is something I'd want to learn from up close. Most of what I know about software I've built from scratch on my own. Understanding how you take large legacy systems and modernize them without breaking everything in the process is a whole different kind of challenge.",
        "role_fit": "Software development and Python engineering",
    },
    {
        "to": "hello@tsl.io",
        "company": "The SilverLogic",
        "contact": "David",
        "why": "I found The SilverLogic while looking into Boca Raton tech companies and the variety of what you build is something that stood out to me. Business automation, AI solutions, mobile apps, enterprise modernization -- working across all of those means the team has to be adaptable and actually good at figuring out new problems quickly. That kind of environment where you're building different things for different clients is exactly what I think I'd learn the most from.",
        "role_fit": "Software development and AI engineering",
    },
    {
        "to": "hello@workstory.team",
        "company": "WorkStory",
        "contact": "Matthew",
        "why": "I came across WorkStory while looking into AI HR tech in Boca Raton and using AI to automate performance reviews is something I thought was a smart target. Performance reviews have a reputation for being a waste of time for everyone involved. Building something AI-powered that makes them actually useful and less painful is solving a problem that basically every company with employees has and I'd want to understand how you built the AI side of that.",
        "role_fit": "AI development and Python",
    },
    {
        "to": "info@ecwcomputers.com",
        "company": "ECW Network & IT Solutions",
        "contact": "Team",
        "why": "I found ECW Network while looking into Deerfield Beach IT companies and the 20-year track record in managed services and cybersecurity is something I respect. There's a lot you can only learn from actually working on real infrastructure for real businesses and understanding what breaks and why. Being around a team with that much experience would fill in gaps that no amount of self-teaching can.",
        "role_fit": "IT infrastructure and cybersecurity",
    },
    {
        "to": "engage@mdlive.com",
        "company": "MDLIVE",
        "contact": "Team",
        "why": "I came across MDLIVE while looking into Miramar healthtech companies and the platform you've built connecting millions of patients to care is something with real stakes. Getting telehealth right technically means everything has to work reliably, securely, and compliantly at the same time. Building and running that kind of platform where the consequences of failure are real is a challenge I'd want to understand from the inside.",
        "role_fit": "Software engineering and healthcare data",
    },
]


def build_email(company: dict) -> str:
    return f"""Hi {company["contact"]},

My name is Gabriel Zebersky and I'm a junior in high school from Cooper City, FL. I'm reaching out because I came across {company["company"]} and wanted to get in touch directly.

{company["why"]}

A bit about what I actually bring to the table: I've been coding in Python for a few years now and it's become my main thing. I use Claude Code for AI-assisted development and I've been building full stack web apps with a tool called Lovable. I know being 17 with no formal job experience sounds like a red flag, but I've built real projects that actually work and I learn new things really fast. I spend most of my free time on this stuff because it's what I want to do with my life and I want to get as much real experience as I can before I graduate.

What I'm really looking for is just real experience. I want to be around people who are actually building things and learn from them up close. I'm completely open to working for free, I don't need a salary or anything like that right now. Even just a few hours a week remotely where I could help with something would be more valuable to me than almost anything school could teach me at this point. I can work around my schedule and I'm pretty flexible.

If there's any chance I could be useful to your team in some way I'd love to hear back. I'm happy to share my projects, put together a portfolio, or jump on a call whenever works for you.

Thanks for taking the time to read this,
Gabriel Zebersky
zeberskygabriel@gmail.com"""


def preview_all():
    print("=" * 60)
    print("EMAIL PREVIEW, review before sending")
    print("=" * 60)
    for i, c in enumerate(companies, 1):
        print(f"\n[{i}/{len(companies)}] TO: {c['to']}")
        print(f"SUBJECT: Internship Inquiry - Gabriel Zebersky | Python & AI")
        print("-" * 40)
        print(build_email(c))
        print()


def send_one(to_email: str, body: str) -> bool:
    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={"api-key": BREVO_API_KEY, "Content-Type": "application/json"},
        json={
            "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
            "to": [{"email": to_email}],
            "subject": "Internship Inquiry - Gabriel Zebersky | Python & AI",
            "textContent": body,
        },
    )
    return response.status_code == 201


def send_all():
    if BREVO_API_KEY == "PASTE_BREVO_API_KEY_HERE":
        print("ERROR: Set your Brevo API key in BREVO_API_KEY first.")
        print("Get it at brevo.com -> Settings -> API Keys")
        return

    sent, failed = [], []

    for c in companies:
        try:
            ok = send_one(c["to"], build_email(c))
            if ok:
                print(f"  SENT -> {c['to']}")
                sent.append(c["to"])
            else:
                print(f"  FAILED -> {c['to']}")
                failed.append(c["to"])
        except Exception as e:
            print(f"  ERROR -> {c['to']}: {e}")
            failed.append(c["to"])

    print(f"\nDone. {len(sent)} sent, {len(failed)} failed.")
    if failed:
        print("Failed:", failed)


if __name__ == "__main__":
    send_all()
