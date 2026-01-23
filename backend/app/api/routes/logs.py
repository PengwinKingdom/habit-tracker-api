from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from datetime import date
from app.db.session import get_db

router=APIRouter(prefix="/habits",tags=["logs"])

class LogCreate(BaseModel):
    log_date:date
    completed:bool=True
    notes:str|None=None

@router.post("/{habit_id}/logs")
def create_log(habit_id:int,payload:LogCreate,db:Session=Depends(get_db)):
    # prevents duplicates for same habit + date
    q=text(""" 
       INSERT INTO dbo.HabitLogs(HabitId,LogDate,Completed,Notes,CreatedAt)
       VALUES (:habit_id, :log_date, :completed, :notes, SYSDATETIME())
    """)
    try:
        db.execute(q,{
            "habit_id":habit_id,
            "log_date":payload.log_date,
            "completed":1 if payload.completed else 0,
            "notes":payload.notes
        })
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=str(e))

    return {"habit_id":habit_id, "log_date":str(payload.log_date),"completed":payload.completed,"notes": payload.notes}
