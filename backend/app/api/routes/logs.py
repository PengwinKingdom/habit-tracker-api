from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from datetime import date
from app.db.session import get_db

#router for habit log operations
router=APIRouter(prefix="/habits",tags=["logs"])

#request for creating a new log
class LogCreate(BaseModel):
    log_date:date
    completed:bool=True
    notes:str|None=None

# request for upsert
class LogUpsert(BaseModel):
    completed:bool=True
    notes:str|None=None

@router.post("/{habit_id}/logs")
def create_log(habit_id:int,payload:LogCreate,db:Session=Depends(get_db)):
    # inserts a new log row and prevents duplicates for same habit + date
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
    
    # return a simple response confirming what was saved
    return {"habit_id":habit_id, "log_date":str(payload.log_date),"completed":payload.completed,"notes": payload.notes}


@router.put("/{habit_id}/logs/{log_date}")
def upsert_log(
    habit_id:int,
    log_date:date,
    payload:LogUpsert,
    db:Session=Depends(get_db)
):
    # verifying the habit exists
    habit_exists=db.execute(
        text("SELECT 1 FROM dbo.Habits WHERE HabitId = :habit_id"),
        {"habit_id":habit_id}
    ).first()
    
    if not habit_exists:
        raise HTTPException(status_code=404,detail=f"Habit {habit_id} not found")
    
    # checking if a log for that habit+date already exists
    exists=db.execute(
        text(""" 
             SELECT 1
             FROM dbo.HabitLogs
             WHERE HabitId = :habit_id AND LogDate = :log_date
             """),
        
        {"habit_id":habit_id,"log_date":log_date}
    ).first()
    
    try:
        if exists:
            #updating log if exists
            db.execute(
                text(""" 
                     UPDATE dbo.HabitLogs
                     SET Completed = :completed,
                      NOTES =: notes
                    WHERE HabitId = :habit_id AND LogDate = :log_date
                    """),
                
                {
                    "habit_id":habit_id,
                    "log_date":log_date,
                    "completed":1 if payload.completed else 0,
                    "notes":payload.notes,
                }
            )
            
            action="updated"
            
        else:
            # create a new log if it doesn't exist yet
            db.execute(
                text(""" 
                     INSERT INTO dbo.HabitLogs (HabitId,LogDate,Completed,Notes,CreatedAt)
                     VALUES (:habit_id, :log_date, :completed, :notes, SYSDATETIME())
                     """),
                
                {
                    "habit_id":habit_id,
                    "log_date":log_date,
                    "completed":1 if payload.completed else 0,
                    "notes":payload.notes,
                }
            )
            
            action="created"
            
        db.commit()
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=str(e))
    
    return {
        "action":action,
        "habit_id":habit_id,
        "log_date":str(log_date),
        "completed":payload.completed,
        "notes":payload.notes
    }

@router.get("/{habit_id}/logs")
def list_logs(habit_id:int,days:int=30,db:Session=Depends(get_db)):
    q=text(""" 
           SELECT HabitLogId,HabitId,LogDate,Completed,Notes,CreatedAt
           FROM dbo.HabitLogs
           WHERE HabitId = :habit_id
            AND LogDate >= DATEADD(DAY, -( :days -1), CAST(GETDATE() AS DATE))
           ORDER BY LogDate DESC
           """)
    
    rows=db.execute(q,{"habit_id":habit_id,"days":days,"logs":list(rows)})