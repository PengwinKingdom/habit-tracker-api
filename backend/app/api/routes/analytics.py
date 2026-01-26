from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db

# router group for analytics endpoints
router=APIRouter(prefix="/users",tags=["analytics"])

@router.get("/{user_id}/analytics/completion")
def completion_rate(user_id:int,days:int=7,db:Session=Depends(get_db)):
    q=text(""" 
      SELECT
       h.HabitId,
       h.Title,
       CAST(
        100.0*SUM(CASE WHEN hl.Completed=1 THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*),0)
        AS DECIMAL(5,2)
       )AS CompletionRate
      FROM dbo.Habits h
      LEFT JOIN dbo.HabitLogs hl
        ON hl.HabitId=h.HabitId
        AND hl.LogDate>=DATEADD(DAY,-( :days - 1 ), CAST(GETDATE() AS DATE))
      WHERE h.UserId=:user_id
      GROUP BY h.HabitId,h.Title
      ORDER BY CompletionRate DESC;
    """)

    rows=db.execute(q,{"user_id":user_id,"days":days}).mappings().all()
    return {"user_id":user_id,"days":days,"results":list(rows)}
  