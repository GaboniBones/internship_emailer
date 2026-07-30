# Internship Emailer

A Python outreach bot that finds internship contacts and sends personalized cold emails at scale, with de-duplication so the same contact is never emailed twice.

## Features

- Automated contact discovery + personalized email sending (`auto_find_and_email.py`)
- Batch sending with rate control (`send_batch.py`, `send_emails.py`)
- Tracks who has already been contacted to avoid duplicates
- One-click run on Windows via `run_bot.bat`

## Requirements

- Python 3.10+
- An email account / SMTP credentials (or an email API key)

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Provide your email credentials via environment variables (never hard-code them):

```bash
export EMAIL_ADDRESS="you@example.com"
export EMAIL_PASSWORD="your-app-password"
```

## Usage

```bash
python auto_find_and_email.py     # discover contacts and email them
python send_batch.py              # send a prepared batch
```

Or on Windows, double-click `run_bot.bat`.

## Notes

- `contacted.json` and `outreach.log` hold contact/PII data and run history — they are **git-ignored** and kept local.
- Follow anti-spam laws (e.g. CAN-SPAM) and each provider's terms. Keep volumes reasonable and include an opt-out.
