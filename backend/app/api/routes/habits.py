from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db

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