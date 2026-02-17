# Habit Tracker (FastAPI + SQL Server + Streamlit)

A habit tracking project with a REST API (FastAPI) and a Streamlit UI to create habits, log daily progress, and generate weekly insights (persisted reports).


## Features
- Users
  - Create users (full name + email)
  - Select active user from the UI
- Habits
  - Create and list habits per user
- Logs
  - Create and update daily logs (completed + notes)
  - Fetch logs for the last N days
- Analytics
  - Completion rate per habit (last N days)
- Weekly Reports
  - Generate weekly summary (insights)
  - Persist reports in SQL Server (MERGE / upsert)
  - View latest report, history, and report details

## Tech Stack
- Backend: FastAPI
- Frontend: Streamlit
- Database: Microsoft SQL Server
- Data access: SQLAlchemy `text()` (raw SQL)

## Project Structure
```bash
habit-tracker-api/
  backend/
  frontend/
  database/
```

## Run locally

### Requirements
- Python 3.11+

### 1) Clone
```bash
git clone https://github.com/PengwinKingdom/habit-tracker-api.git
cd habit-tracker-api
```

### 2) Database (SQL Server)
Run the schema script in SQL Server:
- `database/01_schema.sql`

This creates:
- `dbo.Users`
- `dbo.Habits`
- `dbo.HabitLogs`
- `dbo.WeeklyReports`


### 3) Backend

```bash
cd backend
python -m venv .venv
```

#### For Windows:
```bash
.\.venv\Scripts\activate
```
#### For Mac and Linux:
```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend URL: http://localhost:8000  
API Docs (Swagger): http://localhost:8000/docs


### 4) Frontend (Streamlit)

```bash
cd ../frontend
python -m venv .venv
```

#### For Windows:
```bash
.\.venv\Scripts\activate
```
#### For Mac and Linux:
```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

Frontend URL: http://localhost:8501


## API Endpoints (main)
| Method | Endpoint | Description |
|-------:|----------|-------------|
| POST    | /users  | Create user |
| GET    | /users  | List users |
| GET    | /users/{user_id}  | Get user by id |
| GET    | /users/{user_id}/habits  | List habits for user |
| POST    | /users/{user_id}/habits  | Create habit for user |
| POST    | /habits/{habit_id}/logs  | Create log |
| PUT    | /habits/{habit_id}/logs/{log_date} | Update log |
| GET    | /habits/{habit_id}/logs?days=30  | List recent logs |
| GET | /users/{user_id}/analytics/completion?days=7 | Completion rate per habit |
| POST | /users/{user_id}/insights/weekly-summary | Generate + persist weekly report |
| GET | /users/{user_id}/reports/weekly/latest | Latest report |
| GET | /users/{user_id}/reports/weekly?limit=12 | Report history |
| GET | /users/{user_id}/reports/weekly/{report_id} | Report detail |


## Error Codes
- `404 Not Found` → resource not found (user/habit/report)
- `422 Unprocessable Entity` → missing/invalid request fields
- `409 Conflict` → duplicated resource
