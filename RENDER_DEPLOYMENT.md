# 🚀 Render Deployment Guide (Full System)

This guide provides the complete, step-by-step process for deploying the MOM AI Assistant to [Render.com](https://render.com).

---

## 🏗 Prerequisites
1.  **Render Account**: Sign up at [render.com](https://render.com).
2.  **GitHub Repository**: Ensure your code (both `backend/` and `frontend/` folders) is pushed to a private GitHub repository.
3.  **Google Credentials**: You must have your `google_credentials.json` ready (as explained in `CREDENTIALS_GUIDE.md`).

---

## 📦 1. Preparing the Code for Deployment

### 1.1 Backend (`backend/app/main.py`)
Ensure your CORS settings allow your future frontend URL. For now, you can use `*` to test, but it's better to update it later.

### 1.2 Frontend API Base URL
Ensure your frontend uses an environment variable for the API URL. In `frontend/src/api/index.ts` (or wherever you initialize axios), it should look like:
```typescript
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'
});
```

---

## 🖥 2. Deploying the Backend (Web Service)

1.  Log in to **Render Dashboard**.
2.  Click **New +** > **Web Service**.
3.  Connect your GitHub repository.
4.  **Configure Service**:
    *   **Name**: `mom-backend`
    *   **Runtime**: `Python 3`
    *   **Root Directory**: `backend` (CRITICAL)
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5.  **Environment Variables**:
    Click **Advanced** > **Add Environment Variable** and add ALL keys from your `.env` file:
    *   `OPENAI_API_KEY`: `...`
    *   `ASSEMBLY_AI_API_KEY`: `...`
    *   `SPREADSHEET_ID`: `...`
    *   `DRIVE_FOLDER_ID`: `...`
    *   `SMTP_USER`: `...`
    *   `SMTP_PASSWORD`: `...` (16-char app password)
    *   `CLIENT_NAME`: `...`
    *   `CLIENT_ADDRESS`: `...`
    *   `CLIENT_CS_EMAIL`: `...`
    *   `PORT`: `10000` (Render's default)
6.  **Google Credentials Secret File**:
    *   Go to **Secret Files** tab in Render.
    *   Filename: `google_credentials.json`
    *   Contents: Paste the ENTIRE content of your local `google_credentials.json` file.
7.  Click **Deploy Web Service**.
8.  **Wait**: Note down the URL Render provides (e.g., `https://mom-backend.onrender.com`).

---

## 🌐 3. Deploying the Frontend (Static Site)

1.  Click **New +** > **Static Site**.
2.  Connect the same GitHub repository.
3.  **Configure Site**:
    *   **Name**: `mom-frontend`
    *   **Root Directory**: `frontend` (CRITICAL)
    *   **Build Command**: `npm install && npm run build`
    *   **Publish Directory**: `dist`
4.  **Environment Variables**:
    Click **Advanced** > **Add Environment Variable**:
    *   `VITE_API_BASE_URL`: `https://mom-backend.onrender.com/api/v1` (Paste your Backend URL here + `/api/v1`)
5.  **Redirects/Rewrites**:
    *   Go to **Redirects** tab.
    *   Source: `/*`
    *   Destination: `/index.html`
    *   Action: `Rewrite` (This ensures React Router works after refresh).
6.  Click **Deploy Static Site**.

---

## 🔗 4. Final Connection (CORS Update)

Once your frontend is deployed (e.g., `https://mom-frontend.onrender.com`), you must tell the backend to allow requests from it.

1.  Go to your **Backend Service** on Render.
2.  Go to **Environment Variables**.
3.  Add/Update:
    *   `FRONTEND_URL`: `https://mom-frontend.onrender.com`
4.  The backend will automatically redeploy.

---

## 🛠 Troubleshooting Render

*   **Build Fails**: Check if you set the **Root Directory** correctly (`backend` or `frontend`).
*   **API Errors**: Ensure `VITE_API_BASE_URL` in the frontend has `https://` and ends with `/api/v1`.
*   **Google Auth 403**: Ensure your Render Backend environment variables (Spreadsheet ID, etc.) match exactly.
*   **SMTP Errors**: Check if your Gmail App Password has spaces (it shouldn't).

---
*Botivate Services LLP © 2026. Secure Deployment on Autopilot.*
