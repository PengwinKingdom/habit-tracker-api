from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel, EmailStr

from app.db.session import get_db

router=APIRouter(prefix="/users",tags=["users"])

class UserCreate(BaseModel):
    full_name:str
    email:EmailStr

@router.post("")
def create_user(payload:UserCreate,db:Session=Depends(get_db)):
    q=text(""" 
    INSERT INTO dbo.Users(FullName,Email,CreatedAt)
    OUTPUT INSERTED.UserId, INSERTED.FullName,INSERTED.Email,INSERTED.CreatedAt
    VALUES(:full_name, :email, SYSDATETIME())
    """)

    try:
        row=db.execute(q,{"full_name":payload.full_name,"email":payload.email}).mappings().first()
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=str(e))

    if not row:
        raise HTTPException(status_code=500,detail="Failed to create user")

    return row


@router.get("/{user_id}")
def get_user(user_id:int,db:Session=Depends(get_db)):
    q=text(""" 
    SELECT UserId,FullName,Email,CreatedAt
    FROM dbo.Users
    WHERE UserId = :user_id
    """)

    row=db.execute(q,{"user_id":user_id}).mappings().first()
    if not row:
        raise HTTPException(status_code=404,detail="User not found")
    return row
