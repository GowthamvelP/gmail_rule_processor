import sqlite3
import json
from datetime import datetime
from fetch_emails import get_service

def match_rule(email, rule):
    field = rule['field'].lower()
    value = rule['value']
    predicate = rule['predicate'].lower()
    email_value = email.get(field, '')

    if field == 'received_at':
        email_date = datetime.fromisoformat(email_value)
        now = datetime.now()
        delta = int(value)
        if 'less' in predicate:
            return (now - email_date).days < delta
        if 'greater' in predicate:
            return (now - email_date).days > delta
    else:
        if predicate == 'contains':
            return value.lower() in email_value.lower()
        if predicate == 'does not contain':
            return value.lower() not in email_value.lower()
        if predicate == 'equals':
            return value.lower() == email_value.lower()
        if predicate == 'does not equal':
            return value.lower() != email_value.lower()
    return False

def apply_actions(service, email_id, actions):
    if 'mark_as_read' in actions:
        service.users().messages().modify(userId='me', id=email_id, body={'removeLabelIds': ['UNREAD']}).execute()
    if 'mark_as_unread' in actions:
        service.users().messages().modify(userId='me', id=email_id, body={'addLabelIds': ['UNREAD']}).execute()

def process():
    with open('rules.json') as f:
        config = json.load(f)

    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    c.execute('SELECT * FROM emails')
    rows = c.fetchall()

    service = get_service()

    for row in rows:
        email = {
            'id': row[0],
            'thread_id': row[1],
            'sender': row[2],
            'recipient': row[3],
            'subject': row[4],
            'body': row[5],
            'received_at': row[6],
            'is_read': row[7]
        }
        matches = [match_rule(email, rule) for rule in config['rules']]
        if (config['predicate'].lower() == 'all' and all(matches)) or            (config['predicate'].lower() == 'any' and any(matches)):
            apply_actions(service, email['id'], config['actions'])

    conn.close()

if __name__ == '__main__':
    process()
