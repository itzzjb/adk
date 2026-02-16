from typing import Dict,Any
from google.adk.agents.llm_agent import Agent

# an inmemomy user database
_FAKE_USER_DB: Dict[str, Dict[str, Any]] = {
    "john.doe@company.com": {"name": "John Doe", "department": "Engineering", "status": "active"},
    "jane.smith@company.com": {"name": "Jane Smith", "department": "Marketing", "status": "active"},
    "joe.brown@company.com": {"name": "Joe Brown", "department": "Sales", "status": "inactive"},
    "bob.johnson@company.com": {"name": "Bob Johnson", "department": "HR", "status": "active"},
    "sarah.wilson@company.com": {"name": "Sarah Wilson", "department": "Finance", "status": "active"}
}

# an inmemory service status database
_FAKE_SERVICE_STATUS_DB: Dict[str, Any] = {
    "email": "operational",
    "vpn": "degraded_performance",
    "file_server": "partial_outage",
    "printer": "operational",
    "hr_portal": "major_outage"
}

# There are 3 types of tools 
# Built-in tools: These are tools that come with the ADK, like a web search tool, big query, vertex ai rag etc.
# Custom tools: These are tools that you can build yourself
# Third-party tools: These are tools Open APIs and MCP tools that you can integrate with the ADK.

def lookup_user(email: str) -> dict[str, Any]:
    """Simulate looking up a user in a database."""
    user = _FAKE_USER_DB.get(email.lower())
    if not user:
        return {"status": "error", "message": f"No user found with email {email}"}
    return {"status": "success", "user": {"email": email.lower(), "name": user["name"], "department": user["department"], "status": user["status"]}}

def check_service_status(service_name: str) -> dict[str, Any]:
    """Simulate checking the status of a service."""
    normalized=service_name.strip().lower()
    status = _FAKE_SERVICE_STATUS_DB.get(normalized)
    if not status:
        return {"status": "error", "message": f"No service found with name {service_name}"}
    return {"status": "success", "service": {"name": normalized, "status": status}}


# The user sends a message 
# The LLM reads the instructions, tool defenitions, and the user message, and decides what to do.
# LLM decided to use a specific tool
# ADK executes the tool with the parameters specified by the LLM
# The tool executes and returns the result to the LLM
# The LLM uses the tool result to generate a response to the user

root_agent = Agent(
    model="gemini-2.5-flash",
    name="helpdesk_root_agent",
    description="Smart IT Helpdesk assistant that helps troubleshoot basic IT issues.",
    instruction=(
        "You are a friendly but efficient IT helpdesk assistant for an internal company.\n"
        "\n"
        "Goals:\n"
        "1. Quickly understand the user's problem.\n"
        "2. Ask one or two clarifying questions if needed.\n"
        "3. Give clear, step-by-step instructions they can follow.\n"
        "4. Keep answers concise and practical.\n"
        "\n"
        "Constraints for now:\n"
        "- You do NOT have access to tools yet.\n"
        "- Don't claim to check real systems.\n"
        "- Use phrases like 'Based on common IT practice...' instead of pretending.\n"
    ),
    tools=[lookup_user, check_service_status]  
)
