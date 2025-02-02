# agents/budget_agent.py
from dotenv import load_dotenv

import os
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
from swarm import Agent

instructions = (
    "You are BudgetAgent. Your goal is to minimize cost. Your ideal cost is 80, "
    "and you accept a proposal if the cost is less than or equal to 85. "
    "You will be provided a current proposal in JSON format (for example: "
    '{"cost": 100, "features": 2}) along with the iteration number. '
    "If the proposal meets your criteria (cost ≤ 85), reply with the word ACCEPT. "
    "Otherwise, propose a new solution by lowering the cost gradually toward 80. "
    "Keep the features value unchanged. Your reply must be either the word ACCEPT "
    "or valid JSON representing the new proposal."
)

budget_agent = Agent(
    name="BudgetAgent",
    instructions=instructions,
)
