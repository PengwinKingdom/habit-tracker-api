from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db
from pydantic import BaseModel
from fastapi import HTTPException
from datetime import datetime

# router group for all habits endpoints
router=APIRouter(prefix="/users",tags=["habits"])

@router.get("/{user_id}/habits")
def list_habits(user_id:int,db:Session=Depends(get_db)):
    q=text("""
      SELECT HabitId,Title,Description,IsActive,CreatedAt
      FROM dbo.Habits
      WHERE UserId= :user_id
      ORDER BY CreatedAt DESC
    """)
    rows=db.execute(q,{"user_id":user_id}).mappings().all()
    return{"user_id":user_id,"habits":list(rows)}

class HabitCreate(BaseModel):
  title:str
  description:str | None=None

@router.post("/{user_id}/habits")
def create_habit(user_id:int,payload:HabitCreate,db:Session=Depends(get_db)):
  q=text(""" 
     INSERT INTO dbo.Habits(UserId,Title,Description,IsActive,CreatedAt)
     OUTPUT INSERTED.HabitId,INSERTED.UserId,INSERTED.Title,INSERTED.Description,INSERTED.IsActive,INSERTED.CreatedAt
     VALUES (:user_id, :title, :description,1,SYSDATETIME())
  """)
  row=db.execute(q,{"user_id":user_id,"title":payload.title,"description":payload.description}).mappings().first()
  db.commit()
  if not row:
    raise HTTPException(status_code=500,detail="Failed to create habit")
  return row

