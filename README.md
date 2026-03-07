# MOM AI Assistant

**AI-Powered Minutes of Meeting Management System**

A production-grade full-stack application that converts uploaded MOM documents or manually filled MOM forms into structured meeting records, automatically extracts tasks, assigns responsibilities, sends notifications, tracks progress and attendance, and provides a professional dashboard.

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                    React Frontend                     │
│  (Vite + TypeScript + TailwindCSS + React Query)     │
└────────────────────────┬─────────────────────────────┘
                         │  REST API (JSON)
┌────────────────────────▼─────────────────────────────┐
│                  FastAPI Backend                       │
│  ┌─────────┐  ┌──────────┐  ┌───────────────────┐   │
│  │  Auth   │  │  CRUD    │  │  Upload + AI      │   │
│  │  (JWT)  │  │  APIs    │  │  Pipeline          │   │
│  └─────────┘  └──────────┘  └────────┬──────────┘   │
│                                       │              │
│  ┌────────────────────────────────────▼───────────┐  │
│  │           LangGraph Workflow                    │  │
│  │  ExtractText → CleanText → AIExtraction →      │  │
│  │  Validate → Save → CreateTasks → Notify        │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────┐  ┌────────────┐  ┌─────────────┐  │
│  │ SQLAlchemy   │  │ APScheduler│  │ Notification │  │
│  │ (SQLite/PG)  │  │ (Cron)     │  │ (Email/WA)  │  │
│  └──────────────┘  └────────────┘  └─────────────┘  │
└──────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer          | Technology                                        |
|----------------|---------------------------------------------------|
| Backend        | FastAPI, Python 3.11+, SQLAlchemy, Alembic         |
| AI             | OpenAI GPT-4, LangChain, LangGraph                |
| Frontend       | React 18, TypeScript, Vite, TailwindCSS            |
| State          | Zustand, React Query                               |
| Database       | SQLite (swappable to PostgreSQL)                   |
| Notifications  | SMTP Email, Twilio WhatsApp                        |
| Background     | APScheduler                                        |
| Auth           | JWT (OAuth2 Password Bearer)                       |

---

## Features

- **Two MOM Input Methods**: Upload PDF/TXT or fill manual form
- **AI Extraction**: GPT-4 extracts meeting details, attendees, agenda, action items
- **LangGraph Pipeline**: Multi-node workflow for processing MOMs
- **Task Management**: Auto-create tasks from action items, track status history
- **Attendance Tracking**: Track meeting attendance, warn frequent absentees
- **Notifications**: Email alerts for task assignments, deadlines, overdue items
- **Dashboard**: Stats, charts (Recharts), recent meetings, overdue tasks
- **Role-Based Access**: CEO (full), Manager (meetings+tasks), HR (create+attendance), Employee (view)
- **Dark/Light Mode**: Toggle via top bar
- **Background Jobs**: Scheduled deadline reminders, overdue alerts, absentee warnings

---

## Project Structure

```
MOM_AI_Assistant/
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI routers
│   │   ├── ai/               # AI extraction service
│   │   ├── core/             # Security, auth
│   │   ├── database/         # DB engine, session
│   │   ├── models/           # SQLAlchemy models
│   │   ├── notifications/    # Email, WhatsApp services
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic layer
│   │   ├── workflows/        # LangGraph pipeline
│   │   ├── config.py
│   │   └── main.py
│   ├── alembic/              # Database migrations
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Page components
│   │   ├── api.ts            # Axios instance
│   │   ├── store.ts          # Zustand stores
│   │   ├── types.ts          # TypeScript types
│   │   ├── App.tsx           # Router + layout
│   │   └── main.tsx          # Entry point
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your OpenAI API key and SMTP settings

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` with docs at `http://localhost:8000/docs`.

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

The UI will be available at `http://localhost:5173`.

---

## API Endpoints

| Method | Endpoint                        | Description                  | Auth     |
|--------|---------------------------------|------------------------------|----------|
| POST   | `/api/v1/auth/register`         | Register new user            | Public   |
| POST   | `/api/v1/auth/login`            | Login (returns JWT)          | Public   |
| GET    | `/api/v1/auth/me`               | Current user profile         | Bearer   |
| GET    | `/api/v1/users/`                | List users                   | CEO/HR/Mgr |
| GET    | `/api/v1/meetings/`             | List meetings                | Bearer   |
| POST   | `/api/v1/meetings/`             | Create meeting (manual MOM)  | CEO/HR/Mgr |
| GET    | `/api/v1/meetings/{id}`         | Get meeting detail           | Bearer   |
| POST   | `/api/v1/upload/mom`            | Upload & process MOM file    | CEO/HR/Mgr |
| POST   | `/api/v1/upload/extract-preview`| Preview AI extraction        | CEO/HR/Mgr |
| GET    | `/api/v1/tasks/`                | List tasks (with filters)    | Bearer   |
| PUT    | `/api/v1/tasks/{id}`            | Update task status           | Bearer   |
| GET    | `/api/v1/tasks/{id}/history`    | Task status history          | Bearer   |
| GET    | `/api/v1/attendance/absentees`  | Frequent absentees           | Bearer   |
| GET    | `/api/v1/dashboard/`            | Dashboard analytics          | Bearer   |
| GET    | `/api/v1/notifications/`        | List notifications           | Bearer   |

---

## Database Tables

`users` · `meetings` · `attendees` · `agenda_items` · `discussion_summary` · `tasks` · `task_history` · `notifications` · `next_meetings` · `files`

---

## LangGraph Workflow

```
Upload/Manual Input
       ↓
  ExtractTextNode    ← Extract text from PDF/TXT
       ↓
  CleanTextNode      ← Normalize whitespace, remove artifacts
       ↓
  MOMExtractionNode  ← OpenAI GPT-4 structured extraction
       ↓
  ValidateDataNode   ← Check required fields
       ↓
  [API Layer]        ← Save to DB, create tasks, send notifications
```

---

## Environment Variables

See `backend/.env.example` for all configuration options including:
- `OPENAI_API_KEY` – Required for AI extraction
- `SECRET_KEY` – JWT signing key (change in production!)
- `SMTP_*` – Email notification settings
- `TWILIO_*` – WhatsApp integration settings

---

## License

See [LICENSE](LICENSE) file.