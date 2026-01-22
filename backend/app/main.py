from fastapi import FastAPI
from app.api.routes.habits import router as habits_router

app=FastAPI(title='Habit Tracker API')
app.include_router(habits_router)

@app.get("/health")
def health():
    return{"status":"ok"}