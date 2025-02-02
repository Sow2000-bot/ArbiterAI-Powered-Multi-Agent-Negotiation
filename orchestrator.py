# orchestrator.py

import json
from swarm import Swarm
from agents.budget_agent import budget_agent
from agents.feature_agent import feature_agent
from agents.mediator_agent import mediator_agent
from dotenv import load_dotenv

import os
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
def main():
    # Instantiate the Swarm client.
    client = Swarm()
    
    max_iterations = 10
    current_proposal = {"cost": 100, "features": 2}
    agreement_reached = False
    
    print("Starting negotiation...")
    
    for iteration in range(1, max_iterations + 1):
        print(f"\n--- Iteration {iteration} ---")
        # Create a message that includes the current iteration and proposal.
        message_text = (
            f"Iteration: {iteration}. Current proposal: {json.dumps(current_proposal)}. "
            "Please evaluate and either ACCEPT or propose a new solution."
        )
        
        # --- BudgetAgent Step ---
        response_budget = client.run(
            agent=budget_agent, 
            messages=[{"role": "user", "content": message_text}],
        )
        content_budget = response_budget.messages[-1]["content"].strip()
        print("BudgetAgent response:", content_budget)
        try:
            proposal_from_budget = json.loads(content_budget)
            # Use BudgetAgent's returned proposal if valid JSON.
            current_proposal = proposal_from_budget
            budget_accept = False
        except json.JSONDecodeError:
            budget_accept = content_budget.upper() == "ACCEPT"
        
        # --- FeatureAgent Step ---
        response_feature = client.run(
            agent=feature_agent,
            messages=[{"role": "user", "content": message_text}],
        )
        content_feature = response_feature.messages[-1]["content"].strip()
        print("FeatureAgent response:", content_feature)
        try:
            proposal_from_feature = json.loads(content_feature)
            current_proposal = proposal_from_feature
            feature_accept = False
        except json.JSONDecodeError:
            feature_accept = content_feature.upper() == "ACCEPT"
        
        # Check if both agents accepted the current proposal.
        if budget_accept and feature_accept:
            print("\nAgreement reached!")
            print("Final proposal:", current_proposal)
            agreement_reached = True
            break
        else:
            print("Updated proposal for next round:", current_proposal)
    
    # If no agreement is reached within the allowed iterations, use MediatorAgent.
    if not agreement_reached:
        print("\nNo agreement reached after maximum iterations. MediatorAgent intervenes.")
        message_text = (
            f"Final negotiation attempt. Current proposal: {json.dumps(current_proposal)}. "
            "Please propose a balanced compromise solution."
        )
        response_mediator = client.run(
            agent=mediator_agent,
            messages=[{"role": "user", "content": message_text}],
        )
        mediator_content = response_mediator.messages[-1]["content"].strip()
        try:
            mediator_proposal = json.loads(mediator_content)
            current_proposal = mediator_proposal
            print("MediatorAgent proposal:", current_proposal)
        except json.JSONDecodeError:
            print("MediatorAgent returned an unexpected response:", mediator_content)
    
    print("\nNegotiation complete.")

if __name__ == "__main__":
    main()
