# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)  # 'finder', 'claimer', or 'admin'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    found_items = relationship("Item", back_populates="finder", foreign_keys="Item.finder_id")
    claimed_items = relationship("Item", back_populates="claimer", foreign_keys="Item.claimer_id")
    
    def __repr__(self):
        return f"<User {self.name} ({self.role})>"

class Item(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)
    date_found = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="unclaimed")  # 'unclaimed' or 'claimed'
    date_claimed = Column(DateTime, nullable=True)
    
    finder_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    claimer_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    finder = relationship("User", back_populates="found_items", foreign_keys=[finder_id])
    claimer = relationship("User", back_populates="claimed_items", foreign_keys=[claimer_id])
    
    def __repr__(self):
        return f"<Item {self.description} ({self.status})>"