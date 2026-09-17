# 🕵️ Image Recognition System

A desktop-based **Face recognition and secure criminal records management system** built with Python. The application combines **facial recognition, encrypted biometric embeddings, SQLite database management, secure authentication, case notes, and cryptographically signed audit logs** into a single desktop interface.

The project is designed as a cybersecurity-focused demonstration of how biometric search and database workflows can be combined with security controls.

---

## 📌 Project Overview

The **Image Recognition System** provides a secure desktop application for registering records, comparing faces, searching a database using a face image, maintaining investigation notes, and monitoring system activity through an audit trail.

The application uses **DeepFace with the Facenet512 model** for facial representation and verification. Face embeddings are encrypted before being stored in the SQLite database.

The system also implements:

* Secure administrator authentication
* bcrypt password hashing
* Fernet-based encryption for face embeddings
* HMAC-SHA256 signatures for audit records
* Automatic session locking after inactivity
* Face-to-face similarity verification
* Database face search
* Criminal record registration
* Investigation/case notes
* Audit trail and integrity verification

---

## 🎯 Objectives

The main objectives of this project are:

1. Build an AI-powered face recognition application.
2. Store biometric face embeddings securely.
3. Provide a desktop interface for managing records.
4. Implement secure administrator authentication.
5. Enable image-to-image face comparison.
6. Enable face-based database searching.
7. Maintain investigation notes for registered records.
8. Create an auditable and integrity-verifiable activity trail.

---

## ✨ Features

### 🔐 Secure Login

The application starts with a secure administrator login interface.

Authentication uses:

* Username
* Password
* bcrypt password verification
* Environment-based credential storage
* Audit logging for successful and failed login attempts

Password setup is handled through:

```text
setup_password.py
```

---

### 🧠 AI Face Recognition

The project uses **DeepFace** and the **Facenet512** model to generate facial embeddings and verify faces.

Face representations are generated from uploaded images rather than storing a raw facial feature vector in plaintext.

---

### 📝 Criminal Registration

Module:

```text
cri_reg.py
```

Users can register a record containing:

* Full name
* Age
* Gender
* Father's name
* Crime information
* Face photograph
* Face embedding

The face embedding is encrypted before being stored in the database.

---

### 🖼️ Face Comparison

Module:

```text
img_compare.py
```

The application allows two images to be selected and compared using DeepFace.

The application displays a similarity result and records the comparison event in the audit log.

---

### 🔎 Database Face Search

Module:

```text
show.py
```

A suspect photograph can be uploaded and converted into a face embedding.

The application then:

```text
Suspect Image
      ↓
DeepFace / Facenet512
      ↓
Face Embedding
      ↓
Database Records
      ↓
Decrypt Stored Embeddings
      ↓
Similarity Calculation
      ↓
Top Matching Records
```

The interface displays the top matching database records.

---

### 💬 Case Notes

Module:

```text
chatbox.py
```

Officers can add timestamped investigation notes associated with a registered criminal record.

Each note contains:

* Criminal ID
* Officer name
* Note text
* Timestamp

Notes are stored in the SQLite database.

---

### 🛡️ Audit Trail

Module:

```text
audit_log.py
```

The system records important application activities such as:

* Login success
* Login failure
* Record registration
* Face comparison
* Database search
* Opening application modules
* Password changes
* Session locking
* Case-note creation

Each audit record receives an **HMAC-SHA256 signature**.

The application can also verify stored signatures to detect modifications to audit records.

---

### ⏱️ Automatic Session Lock

The dashboard monitors keyboard and mouse activity.

The configured inactivity timeout is:

```text
300 seconds
```

After inactivity, the session is locked and the login application is started again.

---

### 🔑 Secure Password Management

Administrator passwords are hashed using:

```text
bcrypt
```

The implementation uses a bcrypt work factor of:

```text
12 rounds
```

Password changes are also recorded in the audit trail.

---

## 🧰 Technologies Used

### Programming Language

* Python 3

### GUI

* CustomTkinter
* Tkinter

### Artificial Intelligence / Computer Vision

* DeepFace
* Facenet512
* OpenCV
* NumPy
* Pillow

### Database

* SQLite3

### Security

* bcrypt
* cryptography
* Fernet encryption
* HMAC-SHA256
* SHA-256
* Environment variables using `python-dotenv`

### Logging

* Python `logging` module

---

## 📦 Dependencies

The project specifies the following packages:

```text
customtkinter==5.2.2
deepface==0.0.94
tensorflow==2.16.1
opencv-python-headless==4.10.0.84
Pillow==10.4.0
python-dotenv==1.0.1
bcrypt==4.2.0
cryptography==43.0.1
numpy==1.26.4
```

Install them with:

```bash
pip install -r requirements.txt
```

---

## 🏗️ Project Structure

```text
Image_Recognition_System-main/
│
├── README.md
├── criminals.db
│
├── login.py
├── dashboard.py
├── cri_reg.py
├── img_compare.py
├── show.py
├── chatbox.py
│
├── security.py
├── audit_log.py
├── setup_password.py
│
└── requirements.txt
```

---

## 📂 Module Description

### `login.py`

Responsible for the administrator authentication interface.

Main responsibilities:

* Create login window
* Accept username and password
* Verify password
* Record login success/failure
* Open the dashboard after successful authentication

Main class:

```python
LoginApp
```

---

### `dashboard.py`

Provides the main application dashboard after authentication.

Dashboard functions include:

```text
Criminal Registration
Image Recognition
Case Notes
Database Face Search
Audit Trail
Change Password
```

Main class:

```python
DashboardApp
```

The dashboard also implements the inactivity timeout.

---

### `cri_reg.py`

Handles criminal-record registration.

Main workflow:

```text
Enter Record Information
        ↓
Select Face Image
        ↓
Detect Face
        ↓
Generate Face Embedding
        ↓
Encrypt Embedding
        ↓
Store Record in SQLite
        ↓
Create Audit Entry
```

Main class:

```python
CriminalRegistrationApp
```

---

### `img_compare.py`

Provides face-to-face comparison between two uploaded images.

Workflow:

```text
Image 1
   +
Image 2
   ↓
DeepFace.verify()
   ↓
Similarity / Verification Result
   ↓
Audit Log
```

Main class:

```python
ImageCompareApp
```

---

### `show.py`

Provides AI-powered database face searching.

Workflow:

```text
Upload Suspect Image
        ↓
DeepFace.represent()
        ↓
Generate Face Embedding
        ↓
Read Database Embeddings
        ↓
Decrypt Embeddings
        ↓
Normalize Vectors
        ↓
Calculate Similarity
        ↓
Sort Results
        ↓
Display Top 5
```

Main class:

```python
FaceDatabaseSearchApp
```

---

### `chatbox.py`

Provides investigation/case note management.

Main functions include:

* Load registered records
* Select a criminal record
* Add investigation notes
* Display existing notes
* Timestamp each note
* Create audit records

Main class:

```python
ChatBoxApp
```

---

### `security.py`

Central security module for the application.

It provides:

#### Password Security

```python
hash_password()
verify_password()
update_password_hash()
```

Passwords are protected using bcrypt.

#### Embedding Encryption

```python
encrypt_embedding()
decrypt_embedding()
```

The project uses Fernet symmetric encryption to protect stored face embeddings.

#### Audit Signatures

```python
generate_audit_signature()
verify_audit_signature()
```

These functions generate and verify HMAC-SHA256 signatures for audit records.

#### Logging

```python
log_error()
log_info()
```

Application logs are written to:

```text
logs/system.log
```

---

### `audit_log.py`

Responsible for secure audit logging.

Main functions:

```python
init_audit_table()
log_audit()
verify_audit_logs()
get_audit_trail()
```

Audit records contain:

```text
ID
Timestamp
Officer
Action
Target ID
Details
Signature
```

---

### `setup_password.py`

Command-line utility for setting the initial administrator password.

The password is entered using hidden input and only the bcrypt hash is written to the `.env` file.

Run:

```bash
python setup_password.py
```

---

## 🗄️ Database

The project uses:

```text
criminals.db
```

SQLite database tables include:

### `criminals`

Stores criminal record information and encrypted face embeddings.

```text
id
name
age
gender
father_name
crime
image_path
face_encoding
```

---

### `case_notes`

Stores investigation notes.

```text
id
criminal_id
officer_name
note_text
timestamp
```

The `criminal_id` references the corresponding record in the `criminals` table.

---

### `audit_log`

Stores security and application activity.

```text
id
timestamp
officer_name
action
target_id
details
signature
```

---

## 🔄 System Architecture

```text
                        ┌─────────────────────┐
                        │      login.py       │
                        │ Secure Authentication│
                        └──────────┬──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │    dashboard.py     │
                        │   Main Dashboard    │
                        └───────┬─┬─┬─┬─┬─────┘
                                │ │ │ │ │
              ┌─────────────────┘ │ │ │ └─────────────────┐
              ▼                   │ │ │                   ▼
       ┌─────────────┐            │ │ │          ┌────────────────┐
       │  cri_reg.py │            │ │ │          │   audit_log.py │
       │ Registration│            │ │ │          │  Audit Trail   │
       └──────┬──────┘            │ │ │          └───────┬────────┘
              │                   │ │ │                  │
              ▼                   │ │ │                  ▼
       ┌─────────────┐             │ │ │          ┌────────────────┐
       │  DeepFace   │             │ │ │          │   security.py  │
       │ Facenet512  │             │ │ │          │ Encryption/Auth │
       └──────┬──────┘             │ │ │          └────────────────┘
              │                   │ │ │
              ▼                   │ │ │
       ┌─────────────┐             │ │ │
       │ criminals.db│◄────────────┘ │ │
       └─────────────┘               │ │
                                     │ │
                 ┌───────────────────┘ │
                 ▼                     ▼
        ┌────────────────┐    ┌─────────────────┐
        │ img_compare.py │    │    show.py      │
        │ Face Compare   │    │ DB Face Search  │
        └────────────────┘    └─────────────────┘
                                     
                             ┌─────────────────┐
                             │   chatbox.py    │
                             │   Case Notes    │
                             └─────────────────┘
```

---

## 🔐 Security Architecture

The project uses multiple security mechanisms:

```text
                    Application
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
       bcrypt         Fernet        HMAC-SHA256
       Password       Embeddings     Audit Integrity
          │              │              │
          ▼              ▼              ▼
      .env Hash      Encrypted DB    Signed Logs
```

### Password Protection

Passwords are not stored as plaintext.

```text
Plain Password
      ↓
bcrypt
      ↓
Password Hash
      ↓
.env
```

### Biometric Protection

Face embeddings are encrypted before database storage:

```text
Face Image
    ↓
DeepFace
    ↓
Embedding
    ↓
Fernet Encryption
    ↓
SQLite
```

### Audit Integrity

Audit records receive a cryptographic signature:

```text
Audit Data
    ↓
HMAC-SHA256
    ↓
Signature
    ↓
Database
```

The signature can later be recalculated and compared with the stored signature to identify modifications.

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/Image_Recognition_System.git
```

Go to the project directory:

```bash
cd Image_Recognition_System
```

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Admin Password

Run:

```bash
python setup_password.py
```

Enter and confirm the administrator password.

The password is converted to a bcrypt hash and stored in `.env`.

---

## ▶️ Running the Application

Start the application with:

```bash
python login.py
```

After successful authentication, the main dashboard will open.

---

## 🔑 Application Flow

```text
Run login.py
      ↓
Administrator Login
      ↓
Password Verification
      ↓
Dashboard
      │
      ├── Criminal Registration
      │
      ├── Image Recognition / Face Comparison
      │
      ├── Case Notes
      │
      ├── Database Face Search
      │
      ├── Audit Trail
      │
      └── Change Password
```

---

## 📊 Face Recognition Workflow

### Registration

```text
Upload Image
     ↓
Face Detection
     ↓
Facenet512 Representation
     ↓
Generate Embedding
     ↓
Encrypt Embedding
     ↓
Store in criminals.db
```

### Search

```text
Upload Suspect Image
       ↓
Generate Embedding
       ↓
Retrieve Database Embeddings
       ↓
Decrypt Embeddings
       ↓
Normalize Vectors
       ↓
Calculate Similarity
       ↓
Rank Matches
       ↓
Display Top Results
```

### Face Comparison

```text
Image 1 ─────┐
             ├──► DeepFace.verify()
Image 2 ─────┘
                    ↓
             Verification Result
                    ↓
               Similarity %
```

---

## 📁 Runtime Files

The application may create or use:

```text
.env
logs/system.log
criminals.db
```

### `.env`

Used for security-related configuration such as:

```text
ADMIN_PASSWORD_HASH
FERNET_KEY
AUDIT_HMAC_KEY
```

Do **not** commit `.env` to a public repository.

Recommended `.gitignore` entries:

```gitignore
.env
logs/
__pycache__/
*.pyc
venv/
```

---

## ⚠️ Security and Privacy Considerations

This project handles potentially sensitive biometric and criminal-record data. A production deployment should apply stronger controls than a local demonstration application.

Recommended production improvements include:

* Strong access control and role separation
* Secure key management rather than local `.env` storage
* Database encryption at rest
* Secure backup procedures
* Data-retention policies
* Consent and lawful-use requirements
* Protection of uploaded images
* Stronger input validation
* Secure deployment architecture
* Detailed authorization around biometric searches
* Protection against unauthorized database modification

Face recognition results should also be treated as **decision-support information**, not as definitive identification by themselves.

---

## 🧪 Testing Areas

Important testing areas for this project include:

* Valid and invalid login credentials
* Password update workflow
* Face detection with valid/invalid images
* Face comparison
* Database face search
* Criminal registration
* Case-note creation
* Database integrity
* Audit signature verification
* Session timeout
* Missing configuration keys
* Invalid/corrupted biometric data

---

## 🚀 Future Enhancements

Possible improvements include:

* Multi-user authentication and RBAC
* Admin/officer role separation
* Encrypted database storage
* Secure centralized key management
* Webcam-based live face recognition
* Search filtering and pagination
* Advanced reporting and export
* Better similarity threshold calibration
* Secure cloud deployment
* Centralized audit monitoring
* Database backup and recovery
* Improved error handling and validation
* Privacy-preserving biometric processing

---

## ⚠️ Disclaimer

This project is intended for **educational, research, and authorized demonstration purposes**.

Facial recognition and criminal-record systems involve significant privacy, security, legal, and ethical considerations. The project should only be used with appropriately authorized data and within applicable laws and organizational policies.

---

## 👨‍💻 Author

**Niraj Chaudhari**

MCA Student | Cybersecurity Enthusiast

### GitHub

```text
https://github.com/Nirajbro/
```

---

## ⭐ Project Highlights

```text
✅ Python Desktop Application
✅ AI Face Recognition
✅ DeepFace + Facenet512
✅ SQLite Database
✅ Secure Login
✅ bcrypt Password Hashing
✅ Encrypted Face Embeddings
✅ Fernet Encryption
✅ HMAC-SHA256 Audit Signatures
✅ Tamper Detection
✅ Face Comparison
✅ Database Face Search
✅ Case Notes
✅ Automatic Session Lock
```

---
Note: If you think it is helpful project give star⭐ and stay connected for new projects.
