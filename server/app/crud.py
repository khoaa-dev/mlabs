from . import models, schemas
from sqlalchemy.orm import Session
from .db import db

def create_contact(session: Session, payload: schemas.ContactCreate):
    c = models.Contact(**payload.model_dump())
    session.add(c)
    session.commit()
    session.refresh(c)
    return c

def list_contacts(session: Session):
    return session.query(models.Contact).order_by(models.Contact.id.desc()).all()

def get_contact(session: Session, cid: int):
    return session.query(models.Contact).get(cid)

def update_contact(session: Session, cid: int, payload: schemas.ContactCreate):
    c = get_contact(session, cid)
    if not c: return None
    for k, v in payload.model_dump().items():
        setattr(c, k, v)
    session.commit()
    session.refresh(c)
    return c

def delete_contact(session: Session, cid: int):
    c = get_contact(session, cid)
    if not c: return None
    session.delete(c)
    session.commit()
    return True

def create_message(session: Session, contact_id: int, message_type: str, content: str):
    m = models.Message(contact_id=contact_id, message_type=message_type, content=content)
    session.add(m)
    session.commit()
    session.refresh(m)
    return m

def list_messages(session: Session, cid: int):
    return session.query(models.Message).filter_by(contact_id=cid).order_by(models.Message.created_at.desc()).all()
