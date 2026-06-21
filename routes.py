from fastapi import APIRouter, HTTPException, Depends, status
from models.model import NoteCreate, Note
from database import get_db
from sqlalchemy.orm import Session
from models.user import User, UserCreate, UserLogin
from utils.auth import hash_pw, verify_pw
from utils.jwt_handler import create_access_token
from utils.dependencies import get_current_user

router = APIRouter()

@router.get("/")
def home():
    return {"message": "Notes API"}

@router.get("/notes")
def get_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).all()
    return notes

@router.get("/notes/{note_id}")
def get_single_note(note_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    if note.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this note")
    return note

@router.post("/notes")
def create_note(note: NoteCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    new_note = Note(title=note.title, id=note.id, owner_id = current_user.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return {
        "message": "Note created successfully!",
        "note": {
            "id": new_note.id,
            "title": new_note.title,
            "owner_id": new_note.owner_id
            
        }
    }

@router.delete("/notes/{note_id}")
def delete_Single_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully!"}
              
@router.put("/notes/{note_id}")
def update_note(
    note_id: int,
    updated_note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(
            status_code = 404,
            detail = "Note not found!"
        )
    if note.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this note")
    note.title = updated_note.title
    db.commit()
    db.refresh(note)
    return {"message": "Note updated successfully!", "note": note}
@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()
    if existing_user:
        raise HTTPException(
            status_code = 400,
            detail = "email already registered!"
        )
    new_user = User(
        username = user.username,
        email = user.email,
        password = hash_pw(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return{
        "message" : "user created succesfully!",
        "username": new_user.username,
        "email": new_user.email
    }

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    existing_user =(
        db.query(User).filter(User.email == user.email).first()
    )
    if not existing_user:
        raise HTTPException(
            status_code = 404,
            detail="User Not Found!"
        )
    if not verify_pw(user.password, existing_user.password):
        raise HTTPException(
            status_code = 401,
            detail = "Invalid Password! Try Again."
        )
    token = create_access_token(data={"sub": existing_user.email})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
@router.get("/profile")
def profile(current_user: dict = Depends(get_current_user)):
    return {
        "message": "Welcome to your profile!",
        "user": current_user
    }