# agents/feature_agent.py
from dotenv import load_dotenv

import os
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
from swarm import Agent

instructions = (
    "You are FeatureAgent. Your goal is to maximize features. Your ideal features count "
    "is 4, and you accept a proposal if the features count is at least 3.8. "
    "You will be provided a current proposal in JSON format (for example: "
    '{"cost": 100, "features": 2}) along with the iteration number. '
    "If the proposal meets your criteria (features ≥ 3.8), reply with the word ACCEPT. "
    "Otherwise, propose a new solution by increasing the features gradually toward 4. "
    "When increasing features, assume that each unit increase adds $5 to the cost; adjust the cost accordingly. "
    "Your reply must be either the word ACCEPT or valid JSON representing the new proposal."
)

feature_agent = Agent(
    name="FeatureAgent",
    instructions=instructions,
)
