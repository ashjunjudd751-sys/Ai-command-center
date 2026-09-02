from agents import function_tool

@function_tool
def get_system_status() -> str:
    """Return the current status of the AI dashboard backend."""
    return "AI Command Center backend is online. Database and agent runtime are available."
