from dapr.clients import DaprClient
from dapr.ext.workflow import WorkflowActivityContext
from typing import Dict, Any
import json

def save_state(context: WorkflowActivityContext, input: Dict[str, Any]):
    json_data = json.dumps(input["value"])
    print("BBBAAAAAAALALALALSLALASLA----------------------")
    #print(input)
    #print(json_data)
    try:
        with DaprClient() as d:
            d.save_state(store_name="statestore", key=input["key"], value=json_data)
    except Exception as e:
        print(f"Error saving state: {e}")

def get_state(context: WorkflowActivityContext, input: Dict[str, Any]):
    with DaprClient() as d:
        current_state = d.get_state(store_name="statestore", key=input["key"])

        return json.loads(current_state.data)
