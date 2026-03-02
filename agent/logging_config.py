import logging
import os

# Create a custom logger for the agent
log_file = os.path.join(os.getcwd(), "agent.log")

# Setup formatting
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create a file handler
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)

# Create a stream handler (terminal)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger = logging.getLogger("agent_logger")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def log_agent_action(action: str, details: str = ""):
    """Logs an agent action for auditing."""
    logger.info(f"ACTION: {action} | DETAILS: {details}")

def log_tool_use(tool_name: str, arguments: dict, result: str):
    """Logs a tool use event."""
    logger.info(f"TOOL USE: {tool_name} | ARGS: {arguments} | RESULT: {result[:200]}...")
