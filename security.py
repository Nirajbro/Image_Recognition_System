import os
import logging
import json
import hashlib
import hmac
from dotenv import load_dotenv, set_key
from cryptography.fernet import Fernet
import bcrypt

load_dotenv()

# ------------------ SECURE LOGGING (OPSEC) ------------------
LOG_FILE = "logs/system.log"
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def log_error(msg): logging.error(msg)
def log_info(msg): logging.info(msg)

# ------------------ PASSWORD SECURITY (bcrypt) ------------------
def hash_password(plain_password):
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def update_password_hash(new_plain_password):
    if len(new_plain_password) < 8:
        raise ValueError("Password must be at least 8 characters.")
    new_hash = hash_password(new_plain_password)
    set_key(".env", "ADMIN_PASSWORD_HASH", new_hash)
    log_info("Admin password updated successfully.")
    return True

# ------------------ FACE VECTOR ENCRYPTION (AES-256) ------------------
FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY or FERNET_KEY == "YOUR_GENERATED_FERNET_KEY_HERE":
    FERNET_KEY = Fernet.generate_key().decode()
    set_key(".env", "FERNET_KEY", FERNET_KEY)
    log_info("✅ New Fernet key generated and saved to .env.")
    print("⚠️ Restart the app to load the new Fernet key.")
    exit()

cipher_suite = Fernet(FERNET_KEY.encode())

def encrypt_embedding(embedding_list):
    try:
        json_data = json.dumps(embedding_list)
        encrypted_data = cipher_suite.encrypt(json_data.encode())
        return encrypted_data.decode()
    except Exception as e:
        log_error(f"Encryption failed: {e}")
        return None

def decrypt_embedding(encrypted_string):
    try:
        decrypted_data = cipher_suite.decrypt(encrypted_string.encode())
        return json.loads(decrypted_data.decode())
    except Exception as e:
        log_error(f"Decryption failed: {e}")
        return None

# ------------------ AUDIT HMAC SIGNATURES (Tamper-proof) ------------------
AUDIT_HMAC_KEY = os.getenv("AUDIT_HMAC_KEY")
if not AUDIT_HMAC_KEY or len(AUDIT_HMAC_KEY) < 32:
    new_key = os.urandom(32).hex()
    set_key(".env", "AUDIT_HMAC_KEY", new_key)
    log_info("✅ Auto-generated new AUDIT_HMAC_KEY")
    print("⚠️ Restart the app to load the new audit key.")
    exit()

def generate_audit_signature(record_id, timestamp, action, officer, details):
    message = f"{record_id}|{timestamp}|{action}|{officer}|{details}"
    return hmac.new(AUDIT_HMAC_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()

def verify_audit_signature(record_id, timestamp, action, officer, details, stored_signature):
    message = f"{record_id}|{timestamp}|{action}|{officer}|{details}"
    computed = hmac.new(AUDIT_HMAC_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, stored_signature)