# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)  # 'finder', 'claimer', or 'admin'
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    found_items = relationship("Item", back_populates="finder")
    claims = relationship("Claim", back_populates="claimer")
    
    def __repr__(self):
        return f"<User {self.name} ({self.role})>"

class Item(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)
    date_found = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    finder_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    finder = relationship("User", back_populates="found_items")
    claims = relationship("Claim", back_populates="item", cascade="all, delete-orphan")
    
    @property
    def status(self):
        return "claimed" if any(claim.status == 'approved' for claim in self.claims) else "unclaimed"

    def __repr__(self):
        return f"<Item {self.description} ({self.status})>"

class Claim(Base):
    __tablename__ = 'claims'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    claimer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date_claimed = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String, default="pending") # pending, approved, denied

    item = relationship("Item", back_populates="claims")
    claimer = relationship("User", back_populates="claims")

    def __repr__(self):
        return f"<Claim {self.id} by User {self.claimer_id} for Item {self.item_id}>"
