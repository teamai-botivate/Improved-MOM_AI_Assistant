# ⚙️ Environment Setup & Google Cloud Guide

This document outlines the prerequisites, Google Cloud configuration, local development environment setup, and deployment processes for the **Botivate Agentic MOM System**.

---

## 🛑 Prerequisites

Ensure your system possesses the following dependencies before proceeding:

1. **Node.js** (v18.0.0 or higher) - For React + Vite Frontend
2. **Python** (v3.10.0 or higher) - For FastAPI Backend
3. **Google Account** - To manage Google Sheets and Google Drive storage
4. **Git** - For version control

---

## ☁️ Google Cloud Setup (CRITICAL)

Botivate uses Google Sheets as a database and Google Drive for file archival. Follow these steps exactly to connect the system.

### 1. Create a Google Cloud Project
- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project (e.g., `MOM-AI-Assistant`).

### 2. Enable APIs
Enable the following APIs in your project:
- **Google Sheets API**
- **Google Drive API**

### 3. Create a Service Account
- Navigate to **IAM & Admin > Service Accounts**.
- Click **Create Service Account**.
- Give it a name and click **Create and Continue**.
- Skip optional roles and click **Done**.

### 4. Create and Download JSON Key
- Click on your new Service Account.
- Go to the **Keys** tab.
- Click **Add Key > Create New Key**.
- Select **JSON** and download the file.
- **Rename** this file to `google_credentials.json` and move it to the `backend/` directory of this project.

### 5. Prepare Cloud Storage
- Create a new **Google Sheet**. Copy its **Spreadsheet ID** from the URL:
  `https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit`
- Create a new **Google Drive Folder** to store MOM PDFs. Copy its **Folder ID** from the URL:
  `https://drive.google.com/drive/folders/[FOLDER_ID]`
- **IMPORTANT:** Share both the Google Sheet and the Drive Folder with your **Service Account Email** (e.g., `account-name@project-id.iam.gserviceaccount.com`) as an **Editor**.

---

## 🔑 Environment Secrets Configuration

### Backend (`/backend/.env`)
Create a `.env` file inside the `/backend` directory:

```ini
# App Settings
APP_NAME="Botivate MOM Agent"
API_V1_PREFIX="/api/v1"
CORS_ORIGINS=["http://localhost:5173"]

# Google Cloud Configuration
SPREADSHEET_ID="your_google_sheet_id_here"
DRIVE_FOLDER_ID="your_google_drive_folder_id_here"
GOOGLE_CREDENTIALS_FILE="google_credentials.json"

# AI Configuration (Gemini/OpenAI)
GOOGLE_API_KEY="your_gemini_api_key_here"

# SMTP Mail Configuration (For Automated Dispatch)
MAIL_USERNAME="your-email@gmail.com"
MAIL_PASSWORD="your-app-password"
MAIL_FROM="your-email@gmail.com"
MAIL_PORT=587
MAIL_SERVER="smtp.gmail.com"
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
```

---

## 💻 Local Development Setup

### 1. Backend Initialization (FastAPI)
1. Navigate to `backend/`.
2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1  # Windows
   source .venv/bin/activate     # macOS/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start server:
   ```bash
   uvicorn app.main:app --reload
   ```

### 2. Frontend Initialization (React)
1. Navigate to `frontend/`.
2. Install modules and start:
   ```bash
   npm install
   npm run dev
   ```

---

## 🚀 Troubleshooting
- **403 Forbidden:** Ensure you have shared the Google Sheet and Drive Folder with the Service Account email.
- **Headers Mismatch:** If you modify `SHEET_SCHEMAS` in `google_sheets_service.py`, you must update the header row in your Google Sheet manually.

---
*Botivate Services LLP © 2026. Secure Governance on Autopilot.*
