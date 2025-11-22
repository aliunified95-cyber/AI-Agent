from sqlalchemy.orm import Session
from app.models.db_models import Order, AgentSession, ConversationMessage
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

class DatabaseService:
    def __init__(self, db: Session):
        self.db = db
    
    # Order operations
    def create_order(self, order_data: Dict[str, Any]) -> Order:
        """Create a new order in the database"""
        order = Order(
            order_id=order_data.get("order_id", f"ORDER-{uuid.uuid4().hex[:8]}"),
            customer_name=order_data.get("customer", {}).get("name", ""),
            customer_cpr=order_data.get("customer", {}).get("cpr", ""),
            customer_mobile=order_data.get("customer", {}).get("mobile", ""),
            order_type=order_data.get("order_type", "new_line"),
            line_type=order_data.get("line_details", {}).get("type", "mobile"),
            line_number=order_data.get("line_details", {}).get("number"),
            sub_number=order_data.get("line_details", {}).get("sub_number"),
            device_name=order_data.get("device", {}).get("name") if order_data.get("device") else None,
            device_variant=order_data.get("device", {}).get("variant") if order_data.get("device") else None,
            device_color=order_data.get("device", {}).get("color") if order_data.get("device") else None,
            plan_name=order_data.get("plan", {}).get("name") if order_data.get("plan") else None,
            plan_commitment=order_data.get("plan", {}).get("selected_commitment") if order_data.get("plan") else None,
            financial_type=order_data.get("financial", {}).get("type", "INSTALLMENT"),
            monthly_payment=order_data.get("financial", {}).get("monthly", 0.0),
            advance_payment=order_data.get("financial", {}).get("advance", 0.0),
            upfront_payment=order_data.get("financial", {}).get("upfront", 0.0),
            vat=order_data.get("financial", {}).get("vat", 0.0),
            total_payment=order_data.get("financial", {}).get("total", 0.0),
            accessories=order_data.get("accessories", []),
            order_data=order_data
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """Get order by order_id"""
        return self.db.query(Order).filter(Order.order_id == order_id).first()
    
    def get_order_by_db_id(self, id: str) -> Optional[Order]:
        """Get order by database id"""
        return self.db.query(Order).filter(Order.id == id).first()
    
    # Session operations
    def create_session(self, order_id: str, session_id: str) -> AgentSession:
        """Create a new agent session"""
        order = self.get_order_by_db_id(order_id)
        if not order:
            raise ValueError(f"Order with id {order_id} not found")
        
        session = AgentSession(
            session_id=session_id,
            order_id=order.id,
            state="INIT",
            is_active=True
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def get_session(self, session_id: str) -> Optional[AgentSession]:
        """Get session by session_id"""
        return self.db.query(AgentSession).filter(AgentSession.session_id == session_id).first()
    
    def update_session(self, session_id: str, updates: Dict[str, Any]) -> Optional[AgentSession]:
        """Update session"""
        session = self.get_session(session_id)
        if not session:
            return None
        
        for key, value in updates.items():
            if hasattr(session, key):
                setattr(session, key, value)
        
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def end_session(self, session_id: str) -> Optional[AgentSession]:
        """End a session"""
        return self.update_session(session_id, {
            "is_active": False,
            "ended_at": datetime.utcnow()
        })
    
    # Message operations
    def add_message(self, session_id: str, role: str, content: str, state: str) -> ConversationMessage:
        """Add a conversation message"""
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        message = ConversationMessage(
            session_id=session.id,
            role=role,
            content=content,
            state=state
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
    
    def get_session_messages(self, session_id: str) -> List[ConversationMessage]:
        """Get all messages for a session"""
        session = self.get_session(session_id)
        if not session:
            return []
        
        return self.db.query(ConversationMessage).filter(
            ConversationMessage.session_id == session.id
        ).order_by(ConversationMessage.timestamp).all()

