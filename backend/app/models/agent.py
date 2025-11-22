from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class AgentState(str, Enum):
    INIT = "INIT"
    LANGUAGE_SELECT = "LANGUAGE_SELECT"
    AUTH = "AUTH"
    OWNERSHIP_CHECK = "OWNERSHIP_CHECK"
    ORDER_CONFIRM = "ORDER_CONFIRM"
    MODIFICATION = "MODIFICATION"
    ELIGIBILITY_CHECK = "ELIGIBILITY_CHECK"
    COMMITMENT_APPROVAL = "COMMITMENT_APPROVAL"
    CROSS_SELL = "CROSS_SELL"
    EKYC_SEND = "EKYC_SEND"
    CLOSE = "CLOSE"

class ConversationMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    state: str
    timestamp: Optional[str] = None

class AgentSession(BaseModel):
    session_id: str
    order_data: Dict[str, Any]
    state: AgentState
    conversation_history: List[ConversationMessage]
    language: Optional[str] = None
    customer_authenticated: bool = False
    order_confirmed: bool = False
    order_modified: bool = False

