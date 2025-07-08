import os.path
import base64
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from db import init_db, insert_email
from email.utils import parsedate_to_datetime

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def fetch_emails():
    init_db()
    service = get_service()
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=10).execute()
    messages = results.get('messages', [])

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = msg_data['payload']['headers']
        body = ''
        if 'parts' in msg_data['payload']:
            for part in msg_data['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        else:
            body = base64.urlsafe_b64decode(msg_data['payload']['body'].get('data', '')).decode('utf-8')

        email = {
            'id': msg_data['id'],
            'thread_id': msg_data['threadId'],
            'sender': next((h['value'] for h in headers if h['name'] == 'From'), ''),
            'recipient': next((h['value'] for h in headers if h['name'] == 'To'), ''),
            'subject': next((h['value'] for h in headers if h['name'] == 'Subject'), ''),
            'body': body,
            'received_at': parsedate_to_datetime(next((h['value'] for h in headers if h['name'] == 'Date'), '')).isoformat(),
            'is_read': 0 if 'UNREAD' in msg_data.get('labelIds', []) else 1
        }
        insert_email(email)

if __name__ == '__main__':
    fetch_emails()
