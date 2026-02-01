# Habit Tracker (API + Streamlit Frontend)

A simple habit tracking project with a REST API and a minimal Streamlit UI to create and track habits.


## Features
- Create, list, update and delete habits
- Track daily progress / completions
- Basic validation and clean HTTP errors (404, 409)

## Tech Stack
- Backend:
  * FastAPI
  * Flask
  * Node
    
- Frontend:
  * Streamlit
    
- Storage:
  * SQL
  * JSON
  * in-memory

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


### 3) Frontend (Streamlit)

```bash
cd frontend
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
