# app/__init__.py
from app.database import init_db

__all__ = ['models', 'database', 'cli', 'utils']