from datetime import datetime
from .db import db

# Contact model
class Contact(db.Model):
    __tablename__ = "contacts"
    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(120), nullable=False)
    email   = db.Column(db.String(200))
    company = db.Column(db.String(200))
    role    = db.Column(db.String(120))
    notes   = db.Column(db.Text)

    messages = db.relationship("Message", back_populates="contact", cascade="all, delete-orphan", lazy="selectin")

# Message model
class Message(db.Model):
    __tablename__ = "messages"
    id          = db.Column(db.Integer, primary_key=True)
    contact_id  = db.Column(db.Integer, db.ForeignKey("contacts.id"), nullable=False, index=True)
    message_type= db.Column(db.String(50), nullable=False)
    content     = db.Column(db.Text, nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    contact = db.relationship("Contact", back_populates="messages")
