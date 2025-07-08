# Gmail Rule Processor
A standalone Python script that integrates with Gmail API and performs some rule based operations on emails.

## Setup Instructions

1. Clone the repository
2. Enable Gmail API and download `credentials.json` from Google Cloud Console
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run script to fetch emails:
```bash
python fetch_emails.py
```
5. Edit `rules.json` as needed
6. Run processor:
```bash
python process_emails.py
```

## Testing
```bash
python -m unittest test_rules.py
```

---
