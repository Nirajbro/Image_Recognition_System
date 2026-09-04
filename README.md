# 🕵️ Criminal Face Detection System – Zero-Trust Biometric Security Suite

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Security](https://img.shields.io/badge/Security-AES--256%20%7C%20bcrypt%20%7C%20HMAC-red)](https://cryptography.io)
[![UI](https://img.shields.io/badge/UI-CustomTkinter-darkgreen)](https://customtkinter.tomschimansky.com)

A production-grade, law-enforcement-ready application that combines **AI-powered face recognition** with **military-grade cryptography** (AES-256, bcrypt, HMAC-SHA256 audit logs). Built for cybersecurity professionals and software engineers.

---

## 🚀 Key Features
- **Biometric Face Recognition** (DeepFace – Facenet512) with 99%+ accuracy.
- **AES-256 Encryption** for all stored face embeddings (data at rest).
- **Tamper-Proof Audit Trail** (HMAC-SHA256 signed logs – cannot be forged).
- **Zero-Trust Authentication** (bcrypt hashed passwords, never plaintext).
- **Auto-Lock** (5-min inactivity session timeout).
- **Modern UI** (CustomTkinter dark mode with responsive layout).
- **1-to-1 Comparison** & **1-to-N Database Search**.
- **Case Notes Manager** with timestamped forensic entries.

---

## 🛡️ Security Architecture
| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Auth** | bcrypt (12 rounds) | Passwords are salted & hashed – never stored in plaintext. |
| **Encryption** | Fernet (AES-256-CBC) | Face vectors encrypted before DB insertion. |
| **Integrity** | HMAC-SHA256 | Every audit log is signed – tampering is instantly detected. |
| **Auditing** | SQLite + Forensic Viewer | Full chain-of-custody logging with integrity checker. |

---

## 📦 Installation
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/face-recognition-system.git
cd face-recognition-system

# 2. Install exact dependencies
pip install -r requirements.txt

# 3. Set up your admin password (first time only)
python setup_password.py

# 4. Run the application
python login.py