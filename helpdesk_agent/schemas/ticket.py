from typing import Literal, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Ticket(BaseModel):
    """Schema for an IT helpdesk ticket."""
    ticket_id: str = Field(
        description="Human-readable ID for the ticket, e.g. IT-1A2B3C4D."
    )
    summary: str = Field(
        description="Short summary of the user's issue."
    )
    service: str = Field(
        description="The affected service, e.g. 'email', 'vpn', 'gitlab', 'wifi'."
    )
    user_email: str = Field(
        description="The user's work email address related to this ticket."
    )
    severity: Literal["low", "medium", "high"] = Field(
        default="medium",
        description="Severity of the issue based on impact and urgency.",
    )
    status: Literal["open", "in_progress", "resolved"] = Field(
        default="open",
        description="Current status of the ticket in the helpdesk workflow.",
    )
    department: Optional[str] = Field(
        default=None,
        description="User's department, if known.",
    )
    created_at: datetime = Field(
        description="When the ticket was created (UTC).",
    )