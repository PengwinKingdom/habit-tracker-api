from __future__ import annotations
from datetime import date
from typing import List, Literal, Dict, Any, Tuple
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.db.session import get_db
from sqlalchemy import text, bindparam

router = APIRouter(prefix="/users/{user_id}/insights", tags=["insights"])

class WeeklyInsightsRequest(BaseModel):
    week_start: date
    week_end: date
    language: Literal["en"] = "en"


class WeeklyInsightsResponse(BaseModel):
    summary:str
    highlights: List[str]=Field(default_factory=list)
    next_actions: List[str]=Field(default_factory=list)
    tone:str = "supportive"


def calculate_percentage(part: int, total: int) -> int:
    if total <= 0:
        return 0

    return int (round((part/total) * 100))


@router.post("/weekly-summary", response_model=WeeklyInsightsResponse)
def generate_weekly_insights(user_id:int, req:WeeklyInsightsRequest, db: Session = Depends(get_db)) -> WeeklyInsightsResponse:
    
    q_habits = text(""" 
    SELECT HabitId, Title
    FROM dbo.Habits
    WHERE UserId = :user_id
    """)

    habits_rows = db.execute(q_habits,{"user_id": user_id}).mappings().all()

    if not habits_rows:
        return WeeklyInsightsResponse(
            summary=f"No habits found for user '{user_id}' in the selected week",
            highlights=[],
            next_actions=["Create at least 1 habit to start receiving weekly insights"],
            tone="supportive",
        )

    habit_ids = [row["HabitId"] for row in habits_rows]

    q_logs = text ("""
    SELECT HabitId, COUNT(*) AS Completions
    FROM dbo.HabitLogs
    WHERE HabitId IN :habit_ids
     AND LogDate >= :week_start
     AND LogDate <= :week_end
     AND Completed = 1
    GROUP BY HabitId
    """).bindparams(bindparam("habit_ids", expanding=True))

    log_rows = db.execute(
        q_logs,
        {
            "habit_ids": habit_ids,
            "week_start": req.week_start,
            "week_end": req.week_end,
        },
    ).mappings().all()

    completions_by_habit_id = {hid: 0 for hid in habit_ids}
    for row in log_rows:
        completions_by_habit_id[row["HabitId"]] = int(row["Completions"])

    DEFAULT_GOAL_PER_WEEK = 5

    habits = []
    for row in habits_rows:
        hid = row["HabitId"]
        habits.append(
            {
                "name": row["Title"],
                "goal_per_week": DEFAULT_GOAL_PER_WEEK,
                "completions": completions_by_habit_id.get(hid, 0),
            }
        )

    highlights: List[str] = []
    next_actions: List[str] = []

    # Find strongest / weakest
    habit_scores: List[Tuple[int, Dict[str, Any]]] = []
    for habit in habits:
        completion_rate_pct = calculate_percentage(habit["completions"], habit["goal_per_week"])
        habit_scores.append((completion_rate_pct,habit))
    
    habit_scores.sort(key=lambda item: item[0], reverse=True)

    best_rate, best = habit_scores[0]
    worst_rate, worst = habit_scores[-1]

    highlights.append(f"Best habit: {best['name']} ({best['completions']}/{best['goal_per_week']} = {best_rate}%)")
    highlights.append(f"Main drop: {worst['name']} ({worst['completions']}/{worst['goal_per_week']} = {worst_rate}%)")

    # Simple rule-based actions for worst habit
    if worst_rate < 40:
        next_actions.append(f"Reduce the starting target for {worst['name']} (e.g., 5 minutes) and focus on daily consistency")
        next_actions.append(f"Attach {worst['name']} to a stable trigger")

    elif worst_rate < 70:
        next_actions.append(f"Schedule two short sessions for {worst['name']} on fixed days to reach the weekly goal.")
        next_actions.append(f"Prepare a small ‘setup’ to make starting easier (book ready, timer set).")
    else:
        next_actions.append(f"Keep {worst['name']} consistent and consider increasing the goal slightly next week (+1).")

    summary = (
        f"Weekly summary for user '{user_id}': "
        f"Your strongest habit was {best['name']} ({best_rate}%). "
        f"Focus on improving {worst['name']} ({worst_rate}%) with small, consistent steps."
    )

    return WeeklyInsightsResponse(
        summary=summary,
        highlights=highlights,
        next_actions=next_actions,
        tone="supportive",
    )