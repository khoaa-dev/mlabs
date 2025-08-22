from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from  .. import schemas, crud
from ..db import db

router = Blueprint("contacts", __name__, url_prefix="/contacts")

# Helper function to get a database session
def _session() -> Session:
    return db.session

# Create a new contact
@router.post("")
def create_contact():
    data = request.get_json(force=True) or {}
    try:
        payload = schemas.ContactCreate(**data)       
    except Exception as e:
        return jsonify({"error": "validation_error", "detail": str(e)}), 400
    c = crud.create_contact(_session(), payload)
    out = schemas.ContactOut.model_validate(c)
    return jsonify(out.model_dump()), 201

# List all contacts
@router.get("")
def list_contacts():
    items = crud.list_contacts(_session())
    out = [schemas.ContactOut.model_validate(i).model_dump() for i in items]
    return jsonify(out)

# Get a specific contact
@router.get("/<int:cid>")
def get_contact(cid: int):
    c = crud.get_contact(_session(), cid)
    if not c:
        return jsonify({"error": "Contact not found"}), 404
    out = schemas.ContactOut.model_validate(c).model_dump()
    return jsonify(out)

# Update a contact
@router.put("/<int:cid>")
def update_contact(cid: int):
    data = request.get_json(force=True) or {}
    try:
        payload = schemas.ContactCreate(**data)
    except Exception as e:
        return jsonify({"error": "validation_error", "detail": str(e)}), 400
    c = crud.update_contact(_session(), cid, payload)
    if not c:
        return jsonify({"error": "Contact not found"}), 404
    out = schemas.ContactOut.model_validate(c).model_dump()
    return jsonify(out)

# Delete a contact
@router.delete("/<int:cid>")
def delete_contact(cid: int):
    ok = crud.delete_contact(_session(), cid)
    if not ok:
        return jsonify({"error": "Contact not found"}), 404
    return jsonify({"ok": True})
