from fastapi import APIRouter, HTTPException, status
from models import Note


router = APIRouter()

notes = [
    {"id": 1, "title": "study python"},
    {"id": 2, "title": "study fastapi"}

]
@router.get("/")
def home():
    return {"message": "Notes API"}

@router.get("/notes")
def get_notes():
    return notes

@router.get("/notes/{note_id}")
def get_single_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found!")

@router.post("/notes", status_code=status.HTTP_201_CREATED)
def create_note(note: Note):
    notes.append(note.model_dump())
    return {
        "message": "note added",
        "all_notes": notes
    }
@router.delete("/notes/{note_id}")
def delete_Single_note(note_id: int):
    for note in notes:
        if note["id"]== note_id:
            notes.remove(note)
            return{"success": "note deleted."} 
              
@router.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: dict):
    for note in notes:
        if note["id"]== note_id:
            note["title"] = updated_note["title"]
            return {
                "message": "note updated!",
                "updated_note": note
            }
    return {"error": "note not found!"}