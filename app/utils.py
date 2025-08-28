# app/utils.py
from app.database import Session
from app.models import User, Item

def get_user_by_id(user_id):
    """Get a user by ID"""
    session = Session()
    try:
        return session.query(User).filter(User.id == user_id).first()
    finally:
        Session.remove()

def get_item_by_id(item_id):
    """Get an item by ID"""
    session = Session()
    try:
        return session.query(Item).filter(Item.id == item_id).first()
    finally:
        Session.remove()

def get_all_users():
    """Get all users"""
    session = Session()
    try:
        return session.query(User).all()
    finally:
        Session.remove()

def get_all_items():
    """Get all items"""
    session = Session()
    try:
        return session.query(Item).all()
    finally:
        Session.remove()

def user_exists(email):
    """Check if a user with the given email exists"""
    session = Session()
    try:
        return session.query(User).filter(User.email == email).first() is not None
    finally:
        Session.remove()