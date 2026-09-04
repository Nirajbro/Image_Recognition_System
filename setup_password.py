#!/usr/bin/env python3
"""
Secure Password Setup Utility.
Run this ONCE to set your admin password.
Plaintext password NEVER touches the disk - only the bcrypt hash is stored.
"""
import os
import sys
import getpass
from dotenv import load_dotenv, set_key
import bcrypt

ENV_FILE = ".env"

def hash_password(plain_password):
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')

def main():
    print("=" * 60)
    print("🔐 SECURE PASSWORD SETUP UTILITY")
    print("=" * 60)
    print("This utility will generate a bcrypt hash for your admin password.")
    print("The plaintext password is NEVER saved to disk.")
    print("-" * 60)

    # Load existing .env to preserve other keys (if it exists)
    if os.path.exists(ENV_FILE):
        load_dotenv(ENV_FILE)

    # Prompt for password (input is hidden)
    try:
        password1 = getpass.getpass("Enter new admin password (min 8 chars): ")
        password2 = getpass.getpass("Confirm admin password: ")
    except KeyboardInterrupt:
        print("\n❌ Setup cancelled.")
        sys.exit(1)

    if password1 != password2:
        print("❌ Passwords do not match. Exiting.")
        sys.exit(1)

    if len(password1) < 8:
        print("❌ Password must be at least 8 characters long. Exiting.")
        sys.exit(1)

    # Generate the secure hash
    print("⏳ Hashing password with bcrypt (this takes ~0.5s)...")
    hashed_pw = hash_password(password1)

    # Write ONLY the hash to the .env file
    try:
        set_key(ENV_FILE, "ADMIN_PASSWORD_HASH", hashed_pw)
    except Exception as e:
        print(f"❌ Failed to write to {ENV_FILE}: {e}")
        sys.exit(1)

    print("✅ SUCCESS! bcrypt hash written to .env")
    print("🚀 You can now run 'python login.py' to access the system.")
    print("=" * 60)

if __name__ == "__main__":
    main()