from dapr.ext.workflow import WorkflowActivityContext
from openai import OpenAI
import os
from typing import Dict, Any
import json

def reasoning_activity(context: WorkflowActivityContext, state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Activity function that uses an LLM to determine the next action.
    
    Args:
        context: The workflow activity context
        state: The current state of the workflow
        
    Returns:
        The next action to take
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Prepare the prompt for the LLM
    prompt = f"""
    Current state:
    Input: {state['input']}
    Previous thoughts: {state['thoughts']}
    Previous actions: {state['actions']}
    Previous results: {state['results']}

    Based on this information, what should be the next action?
    Respond in JSON format with the following structure:
    {{
        "thoughts": "Your reasoning about what to do next",
        "type": "action_type",
        "data": {{
            "prompt": "The prompt for the action"
        }}
    }}
    If the task is complete, set "type" to "complete".
    If the task is waiting for user input, set "type" to "user_input".
    These are the only allowed values for "type". Don't try to use any other values.
    """

    # Call the LLM
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant that helps determine the next action in a workflow."},
            {"role": "user", "content": prompt}
        ],
    )

    # Parse the response
    result = json.loads(response.choices[0].message.content)
    return result 

def action_activity(context: WorkflowActivityContext, prompt: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You will try to the best of your ability to give the user the best answer possible"},
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content