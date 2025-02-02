# agents/mediator_agent.py
import os 
from dotenv import load_dotenv

import os
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
from swarm import Agent

instructions = (
    "You are MediatorAgent. You step in when no agreement is reached after the maximum "
    "number of negotiation rounds. Provide a balanced compromise proposal that has a moderate cost "
    "(around 85) and sufficient features (4). Your reply must be valid JSON (for example: "
    '{"cost": 85, "features": 4}).'
)

mediator_agent = Agent(
    name="MediatorAgent",
    instructions=instructions,
)
