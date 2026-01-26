from fastapi import FastAPI
from app.api.routes.habits import router as habits_router
from app.api.routes.logs import router as logs_router
from app.api.routes.analytics import router as analytics_router

# create the FastAPI application instance
app=FastAPI(title='Habit Tracker API')

# registering all API routers
app.include_router(habits_router)
app.include_router(logs_router)
app.include_router(analytics_router)

@app.get("/health")
def health():
    return{"status":"ok"}