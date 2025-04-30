from dapr.ext.workflow import DaprWorkflowContext
from typing import Dict, Any
from activities.state import save_state, get_state
from activities.agent import reasoning_activity, action_activity
import logging

logger = logging.getLogger(__name__)

def agent_workflow(context: DaprWorkflowContext, input: Dict[str, Any]):
    """
    Main workflow function that orchestrates the agent's actions.
    
    Args:
        context: The Dapr workflow context
        input: The input for the workflow
        
    Returns:
        The final state of the workflow
    """
    # Initialize agent memory
    memory = {
        "input": input,
        "thoughts": [],
        "actions": [],
        "results": []
    }

    # Save initial state
    yield context.call_activity(save_state, input={
        "key": context.instance_id,
        "value": memory
    })

    # Main reasoning loop
    max_iterations = 5
    while len(memory["actions"]) < max_iterations:
        # Get current state

        current_state = yield context.call_activity(get_state, input={
            "key": context.instance_id
        })
        
        # Reason about next action
        next_action = yield context.call_activity(
            reasoning_activity,
            input=current_state
        )
        
        # Execute the action
        if next_action.get("type") == "user_input":
            print("Waiting for user input:", next_action.get("data", {}).get("prompt"))
            result = yield context.wait_for_external_event("user_input")
            print("User input received:", result)
        elif next_action.get("type") == "complete":
            print("final action:", next_action)
            break
        else:
            try:
                result = yield context.call_activity(
                    action_activity,
                    input=next_action["data"]["prompt"]
                )
            except Exception as e:
                logger.error(f"Error executing action: {e}, {next_action}")
                raise e
        
        # Update memory
        memory["thoughts"].append(next_action.get("thoughts", ""))
        memory["actions"].append(next_action)
        memory["results"].append(result)
        
        # Save updated state
        yield context.call_activity(save_state, input={
            "key": context.instance_id,
            "value": memory
        })

    return memory 