from fastapi import APIRouter, HTTPException, Depends, status
from models import NoteCreate, Note
from database import get_db
from sqlalchemy.orm import Session


router = APIRouter()

@router.get("/")
def home():
    return {"message": "Notes API"}

@router.get("/notes")
def get_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).all()
    return notes

@router.get("/notes/{note_id}")
def get_single_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note

@router.post("/notes")
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(title=note.title, id=note.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return {
        "message": "Note created successfully!",
        "note": {
            "id": new_note.id,
            "title": new_note.title
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
    db: Session = Depends(get_db)
):
    note = db.query(Note),filter(Note.id==note.id).first()
    if note is None:
        raise HTTPException(
            status_code = 404,
            detail = "Note not found!"
        )
    note.title = updated_note.title
    db.commit()
    db.refresh(note)
    return {"message": "Note updated successfully!", "note": note}