from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text, bindparam
from app.db.session import get_db
from datetime import date, timedelta
import json

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
  

@router.post("/{user_id}/insights/weekly-summary")
def weekly_summary(user_id: int, db: Session = Depends(get_db)):
  week_end: date = date.today()
  week_start: date = week_end - timedelta(days=6)

  habits_q = text(""" 
  SELECT HabitId, Title
  FROM dbo.Habits
  WHERE UserId = :user_id AND IsActive = 1
  ORDER BY CreatedAt ASC;
  """)

  habits = db.execute(habits_q,{"user_id":user_id}).mappings().all()

  if not habits:
    raise HTTPException(status_code=404, detail="User has no active habits")

  habit_ids = [h["HabitId"] for h in habits]

  logs_q = (
    text("""
    SELECT HabitId, LogDate, Completed
    FROM dbo.HabitLogs
    WHERE HabitId IN :habit_ids
      AND LogDate >= :week_start
      AND LogDate <= :week_end;
      """)
      .bindparams(bindparam("habit_ids", expanding=True))
  )

  logs = db.execute(
    logs_q,
    {"habit_ids": habit_ids, "week_start": week_start, "week_end": week_end}
    ).mappings().all()


  completed_by_habit = {hid: 0 for hid in habit_ids}
  total_completed = 0

  for row in logs:
    if row["Completed"] == 1:
      total_completed += 1
      completed_by_habit[row["HabitId"]] += 1

  
  top_habit = max(habits,key=lambda h: completed_by_habit.get(h["HabitId"],0))
  top_count = completed_by_habit.get(top_habit["HabitId"],0)

  highlights = []
  next_actions = []

  highlights.append(f"You completed {total_completed} habits this week")
  if top_count > 0:
    highlights.append(f"Your most constant habit was '{top_habit['Title']}' with {top_count} completed")
  else:
    highlights.append("You haven't marked any habits as completed this week")

  next_actions.append("Choose 1 habit and complete it 2 days in a row")
  next_actions.append("Log your habit after completing it")

  summary = f"Weekly summary ({week_start} - {week_end}): {total_completed} completed logs across {len(habits)} habits"

  result = {
    "summary": summary,
    "highlights": highlights,
    "next_actions": next_actions,
    "tone": "supportive",
    "week_start": str(week_start),
    "week_end": str(week_end),
  }

  merge_q = text(""" 
  MERGE dbo.WeeklyReports AS target
  USING (
   SELECT :UserId AS UserId, :WeekStartDate AS WeekStartDate, :WeekEndDate AS WeekEndDate
   ) AS source
   ON (
    target.UserId = source.UserId
    AND target.WeekStartDate = source.WeekStartDate
    AND target.WeekEndDate = source.WeekEndDate
    )
    WHEN MATCHED THEN
     UPDATE SET
      Summary = :Summary,
      Highlights = :Highlights,
      NextActions = :NextActions,
      Tone = :Tone,
      CreatedAt = SYSUTCDATETIME()
    
    WHEN NOT MATCHED THEN
     INSERT (UserId, WeekStartDate, WeekEndDate, Summary, Highlights, NextActions, Tone)
     VALUES (:UserId, :WeekStartDate, :WeekEndDate, :Summary, :Highlights, :NextActions, :Tone)
    OUTPUT inserted.ReportId;
  """)

  params = {
    "UserId": user_id,
    "WeekStartDate": week_start,
    "WeekEndDate": week_end,
    "Summary": result["summary"],
    "Highlights": json.dumps(result["highlights"], ensure_ascii=False),
    "NextActions": json.dumps(result["next_actions"], ensure_ascii=False),
    "Tone": result["tone"],
  }

  report_id = db.execute(merge_q,params).scalar()
  db.commit()

  result["report_id"] = report_id
  return result



@router.get("/{user_id}/reports/weekly")
def list_weekly_reports(user_id: int, limit: int = 12, db: Session = Depends(get_db)):
  limit = max(1, min(limit, 50))

  q = text("""
    SELECT TOP (:limit)
      ReportId, WeekStartDate, WeekEndDate, Tone, CreatedAt
    FROM dbo.WeeklyReports
    WHERE UserId = :user_id
    ORDER BY CreatedAt DESC;
  """)

  rows = db.execute(q, {"user_id": user_id, "limit": limit}).mappings().all()
  return {"user_id": user_id, "items": list(rows)}



@router.get("/{user_id}/reports/weekly/latest")
def latest_weekly_report(user_id: int, db: Session = Depends(get_db)):
  q = text("""
    SELECT TOP 1
      ReportId, UserId, WeekStartDate, WeekEndDate,
      Summary, Highlights, NextActions, Tone, CreatedAt
    FROM dbo.WeeklyReports
    WHERE UserId = :user_id
    ORDER BY CreatedAt DESC;
  """)

  row = db.execute(q, {"user_id": user_id}).mappings().first()
  if not row:
    raise HTTPException(status_code=404, detail="No weekly reports found.")

  data = dict(row)
  data["summary"] = data.pop("Summary")
  data["highlights"] = json.loads(data.pop("Highlights"))
  data["next_actions"] = json.loads(data.pop("NextActions"))
  data["tone"] = data.pop("Tone")
  return data



@router.get("/{user_id}/reports/weekly/{report_id}")
def get_weekly_report(user_id: int, report_id: int, db: Session = Depends(get_db)):
  q = text("""
    SELECT
      ReportId, UserId, WeekStartDate, WeekEndDate,
      Summary, Highlights, NextActions, Tone, CreatedAt
    FROM dbo.WeeklyReports
    WHERE UserId = :user_id AND ReportId = :report_id;
  """)

  row = db.execute(q, {"user_id": user_id, "report_id": report_id}).mappings().first()
  if not row:
    raise HTTPException(status_code=404, detail="Weekly report not found.")

  data = dict(row)
  data["summary"] = data.pop("Summary")
  data["highlights"] = json.loads(data.pop("Highlights"))
  data["next_actions"] = json.loads(data.pop("NextActions"))
  data["tone"] = data.pop("Tone")
  return data
