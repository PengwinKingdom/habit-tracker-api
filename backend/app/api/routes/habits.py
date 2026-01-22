from fastapi import APIRouter

router=APIRouter(prefix="/users",tags=["habits"])

@router.get("/{user_id}/habits")
def list_habits(user_id:int):
    return{"user_id":user_id,"habits":[]}