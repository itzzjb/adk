from typing import Dict, Any, Literal
from datetime import datetime, timezone
import uuid

from pydantic import BaseModel, Field

from schemas.ticket import Ticket


_FAKE_USER_DIRECTORY: Dict[str, Dict[str, Any]] = {
    "alice@example.com": {
        "name": "Alice Johnson",
        "department": "Engineering",
        "status": "active",
    },
    "bob@example.com": {
        "name": "Bob Smith",
        "department": "Finance",
        "status": "active",
    },
    "carol@example.com": {
        "name": "Carol Lee",
        "department": "HR",
        "status": "locked",
    },
}

_FAKE_SERVICE_STATUS: Dict[str, str] = {

    "email": "operational",
    "vpn": "degraded",
    "gitlab": "outage",
    "wifi": "operational",
}

def lookup_user_impl(email: str) -> Dict[str, Any]:
    """Look up a user in the internal directory.

    Args:
        email: The user's work email address.

    Returns:
        dict: A result object with:
          - status: 'success' or 'error'
          - user:   user details if found
          - error_message: explanation when status='error'
    """
    user = _FAKE_USER_DIRECTORY.get(email.lower())
    if not user:
        return {
            "status": "error",
            "error_message": f"No user found for email '{email}'.",
        }

    return {
        "status": "success",
        "user": {
            "email": email.lower(),
            "name": user["name"],
            "department": user["department"],
            "status": user["status"],
        },
    }

def check_service_status_impl(service_name: str) -> Dict[str, Any]:
    """Check the status of a named IT service.

    Args:
        service_name: Name of the service, e.g. 'email', 'vpn', 'gitlab', 'wifi'.

    Returns:
        dict: A result object with:
          - status: 'success' or 'error'
          - service: normalized service name (when successful)
          - status_text: 'operational', 'degraded', 'outage', etc.
          - error_message: explanation when status='error'
    """
    try:
        normalized = service_name.strip().lower()
        status = _FAKE_SERVICE_STATUS.get(normalized)
        if not status:
            return {
                "status": "error",
                "error_message": (
                    f"Unknown service '{service_name}'. "
                    f"Known services: {', '.join(sorted(_FAKE_SERVICE_STATUS.keys()))}."
                ),
            }

        return {
            "status": "success",
            "service": normalized,
            "status_text": status,
        }
    except Exception as exc:
        return {
            "status": "error",
            "error_message": (
                "Internal error while checking service status: "
                "Please try again later or contact IT."
                f"(Technical details: {type(exc).__name__})"
            ),
        }

class CreateTicketArgs(BaseModel):
    """Arguments for the create_ticket tool."""

    summary: str = Field(
        description="Short summary of the issue, in the user's own words."
    )
    service: str = Field(
        description="The affected service, e.g. 'email', 'vpn', 'gitlab', 'wifi'."
    )
    user_email: str = Field(
        description="The user's work email address."
    )
    severity: Literal["low", "medium", "high"] = Field(
        default="medium",
        description="Severity of the issue based on impact and urgency.",
    )
    department: str | None = Field(
        default=None,
        description="User's department, if known.",
    )

def create_ticket_impl(args: CreateTicketArgs) -> Dict[str, Any]:
    """Create a new IT helpdesk ticket.

    The LLM should call this tool when:
      - The issue is serious enough to track, OR
      - The user explicitly asks to open a ticket, OR
      - Troubleshooting steps did not fully resolve the problem.

    Args:
        args: Structured ticket arguments coming from the LLM.

    Returns:
        dict: A structured ticket object:
          - status: 'success'
          - ticket: Ticket data matching the Ticket schema
    """
    ticket_id = f"IT-{uuid.uuid4().hex[:8].upper()}"
    ticket = Ticket(
        ticket_id=ticket_id,
        summary=args.summary,
        service=args.service.lower(),
        user_email=args.user_email.lower(),
        severity=args.severity,
        status="open",
        department=args.department,
        created_at=datetime.now(timezone.utc),
    )
    return {
        "status": "success",
        "ticket": ticket.model_dump(),
    }
