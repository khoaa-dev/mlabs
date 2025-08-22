# server/app/router/messages.py
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
import asyncio

from .. import schemas, crud, services
from ..db import db

router = Blueprint("messages", __name__, url_prefix="/messages")


def _session() -> Session:
    return db.session

# Generate a message via Ollama and return it for preview
@router.post("/preview")
def preview_message():
    data = request.get_json(force=True) or {}
    try:
        payload = schemas.MessageCreate(**data)  # includes contact_id, message_type, prompt_hint
    except Exception as e:
        return jsonify({"error": "validation_error", "detail": str(e)}), 400

    c = crud.get_contact(_session(), payload.contact_id)
    if not c:
        return jsonify({"error": "Contact not found"}), 404

    context = f"Recipient: {c.name}, Company: {c.company}, Role: {c.role}."
    try:
        text = asyncio.run(
            services.generate_message_from_ollama(
                payload.message_type, context, payload.prompt_hint
            )
        )
    except Exception:
        text = f"[Ollama unavailable] {context}"

    # Return a preview structure — NO DB write
    return jsonify({
        "preview": True,
        "contact_id": c.id,
        "message_type": payload.message_type,
        "content": text
    }), 200

# Fetch message history for a contact.
@router.get("/contact/<int:cid>")
def history(cid: int):
    c = crud.get_contact(_session(), cid)
    if not c:
        return jsonify({"error": "Contact not found"}), 404

    items = crud.list_messages(_session(), cid)
    out = [schemas.MessageOut.model_validate(i).model_dump() for i in items]
    return jsonify(out)

# Save a manual/edited message for a contact (no generation step).
@router.post("/contact/<int:cid>")
def save_for_contact(cid: int):
    data = request.get_json(force=True) or {}
    msg_type = data.get("message_type")
    content = data.get("content")

    if not msg_type or not content:
        return (
            jsonify(
                {
                    "error": "validation_error",
                    "detail": "Both 'message_type' and 'content' are required",
                }
            ),
            400,
        )

    c = crud.get_contact(_session(), cid)
    if not c:
        return jsonify({"error": "Contact not found"}), 404

    m = crud.create_message(_session(), c.id, msg_type, content)
    out = schemas.MessageOut.model_validate(m).model_dump()
    return jsonify(out), 201
