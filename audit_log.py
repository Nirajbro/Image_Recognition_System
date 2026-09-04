import sqlite3
from datetime import datetime
import security

DB_NAME = "criminals.db"


def init_audit_table():
    """Initializes the audit_log table and ensures the signature column exists."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS audit_log
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           timestamp
                           TEXT
                           NOT
                           NULL,
                           officer_name
                           TEXT
                           NOT
                           NULL,
                           action
                           TEXT
                           NOT
                           NULL,
                           target_id
                           INTEGER,
                           details
                           TEXT,
                           signature
                           TEXT
                           NOT
                           NULL
                       )
                       ''')

        # Migration check for older databases lacking the signature column
        cursor.execute("PRAGMA table_info(audit_log)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'signature' not in columns:
            cursor.execute('ALTER TABLE audit_log ADD COLUMN signature TEXT')
            security.log_info("🛡️ Added 'signature' column to audit_log (migration).")

        conn.commit()
        conn.close()
        security.log_info("Audit table initialized with tamper-proof HMAC.")
    except Exception as e:
        security.log_error(f"Audit table init failed: {e}")


def log_audit(officer_name, action, target_id=None, details=""):
    """Logs a new audit entry with a cryptographic signature."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        details_str = str(details)[:500]  # Truncate details to 500 chars to prevent DB issues

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Insert placeholder signature initially to get the auto-increment ID
        cursor.execute('''
                       INSERT INTO audit_log (timestamp, officer_name, action, target_id, details, signature)
                       VALUES (?, ?, ?, ?, ?, ?)
                       ''', (timestamp, officer_name, action, target_id, details_str, "PENDING"))

        record_id = cursor.lastrowid

        # Generate real signature using the actual ID
        signature = security.generate_audit_signature(record_id, timestamp, action, officer_name, details_str)

        # Update the row with the real signature
        cursor.execute('UPDATE audit_log SET signature = ? WHERE id = ?', (signature, record_id))

        conn.commit()
        conn.close()
        security.log_info(f"AUDIT: {officer_name} -> {action} (Target: {target_id})")
    except Exception as e:
        security.log_error(f"Audit write failed: {e}")


def verify_audit_logs():
    """Checks all logs for tampering. Returns (list_of_tampered_ids, total_count)."""
    tampered = []
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, timestamp, officer_name, action, target_id, details, signature FROM audit_log ORDER BY id')
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            rid, ts, officer, action, target, details, sig = row
            if not security.verify_audit_signature(rid, ts, action, officer, details, sig):
                tampered.append(rid)

        return tampered, len(rows)
    except Exception as e:
        security.log_error(f"Audit verification failed: {e}")
        return [], 0


def get_audit_trail(limit=100):
    """Fetches the most recent audit logs."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT id, timestamp, officer_name, action, target_id, details, signature
                       FROM audit_log
                       ORDER BY id DESC LIMIT ?
                       ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        security.log_error(f"Audit fetch failed: {e}")
        return []


# Initialize the table when the module is imported
init_audit_table()