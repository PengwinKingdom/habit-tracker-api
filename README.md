# Habit Tracker (API + Streamlit Frontend)

A simple habit tracking project with a REST API and a minimal Streamlit UI to create and track habits


## Features
- Create, list, update and delete habits
- Track daily progress / completions
- Basic validation and clean HTTP errors (404, 409)

## Tech Stack
- Backend: FastAPI
- Frontend: Streamlit
- Storage: SQLite (local database)

## Run locally

### Requirements
- Python 3.11+

### 1) Clone
```bash
git clone https://github.com/PengwinKingdom/habit-tracker-api.git
cd habit-tracker-api
```

### 2) Backend

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


### 3) Frontend (Streamlit)

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
| GET    | /habits  | List habits |
| POST   | /habits  | Create habit |
| GET    | /habits/{id} | Get habit by id |
| PUT/PATCH | /habits/{id} | Update habit |


## Error Codes
- `404 Not Found` → habit not found
- `409 Conflict` → duplicated resource / invalid state
