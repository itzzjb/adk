from typing import Any
from google.adk.agents.llm_agent import Agent


# There are 3 types of tools 
# Built-in tools: These are tools that come with the ADK, like a web search tool, big query, vertex ai rag etc.
# Custom tools: These are tools that you can build yourself
# Third-party tools: These are tools Open APIs and MCP tools that you can integrate with the ADK.

def lookup_user(email: str) -> dict[str, Any]:
    """Mock function to lookup user information based on email."""
    # In a real implementation, this would query a database or an API.
    return {"status": "success", "user": {"name": "John Doe", "email": email, "department": "Engineering"}}

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
    tools=[]  # We'll add tools in Module 2
)
