from sqlalchemy import Column, String, Integer, Boolean, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String, unique=True, nullable=False, index=True)
    customer_name = Column(String, nullable=False)
    customer_cpr = Column(String, nullable=False)
    customer_mobile = Column(String)
    order_type = Column(String, nullable=False)  # new_line, existing_line, cash
    line_type = Column(String)  # mobile, fiber
    line_number = Column(String)
    sub_number = Column(String)
    device_name = Column(String)
    device_variant = Column(String)
    device_color = Column(String)
    plan_name = Column(String)
    plan_commitment = Column(String)
    financial_type = Column(String)  # INSTALLMENT, SUBSIDY
    monthly_payment = Column(Float, default=0.0)
    advance_payment = Column(Float, default=0.0)
    upfront_payment = Column(Float, default=0.0)
    vat = Column(Float, default=0.0)
    total_payment = Column(Float, default=0.0)
    accessories = Column(JSON, default=list)
    order_data = Column(JSON)  # Full order data as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    sessions = relationship("AgentSession", back_populates="order")

class AgentSession(Base):
    __tablename__ = "agent_sessions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, unique=True, nullable=False, index=True)
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)
    state = Column(String, nullable=False, default="INIT")
    language = Column(String)  # ar, en
    customer_authenticated = Column(Boolean, default=False)
    order_confirmed = Column(Boolean, default=False)
    order_modified = Column(Boolean, default=False)
    customer_name = Column(String)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    
    # Relationships
    order = relationship("Order", back_populates="sessions")
    messages = relationship("ConversationMessage", back_populates="session", cascade="all, delete-orphan")

class ConversationMessage(Base):
    __tablename__ = "conversation_messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("agent_sessions.id"), nullable=False)
    role = Column(String, nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    state = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("AgentSession", back_populates="messages")

