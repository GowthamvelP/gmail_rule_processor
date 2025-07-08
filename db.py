import sqlite3

def init_db():
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            thread_id TEXT,
            sender TEXT,
            recipient TEXT,
            subject TEXT,
            body TEXT,
            received_at TEXT,
            is_read INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_email(email):
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO emails VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (
        email['id'], email['thread_id'], email['sender'], email['recipient'],
        email['subject'], email['body'], email['received_at'], email['is_read']
    ))
    conn.commit()
    conn.close()
