from fastapi import FastAPI, HTTPException
from dapr.ext.workflow import DaprWorkflowClient
from dapr.clients import DaprClient
from workflows.agent_workflow import agent_workflow
from typing import Dict, Any
import uuid
import logging

logger = logging.getLogger(__name__)

app = FastAPI()
workflow_client = DaprWorkflowClient()
dapr_client = DaprClient()

@app.post("/start")
async def start_workflow(input_data: Dict[str, Any]):
    try:
        # Generate a unique workflow ID
        workflow_id = str(uuid.uuid4())
        logger.info(f"Starting new workflow with ID: {workflow_id}")
        
        # Start the workflow
        instance_id = workflow_client.schedule_new_workflow(
            workflow=agent_workflow,
            input=input_data,
            instance_id=workflow_id
        )
        
        logger.info(f"Successfully started workflow {workflow_id} with instance ID: {instance_id}")
        return {"workflow_id": workflow_id, "instance_id": instance_id}
    except Exception as e:
        logger.error(f"Error starting workflow: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/{workflow_id}")
async def get_workflow_state(workflow_id: str):
    try:
        logger.info(f"Getting status for workflow: {workflow_id}")
        # Get workflow status
        state = workflow_client.get_workflow_state(workflow_id)
        if not state:
            logger.warning(f"No workflow state found for ID: {workflow_id}")
            raise HTTPException(status_code=404, detail="Workflow not found")
        logger.info(f"Retrieved status for workflow {workflow_id}: {state}")
        return state
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting workflow status: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/pause/{workflow_id}")
async def pause_workflow(workflow_id: str):
    try:
        logger.info(f"Pausing workflow: {workflow_id}")
        workflow_client.pause_workflow(workflow_id)
        logger.info(f"Successfully paused workflow {workflow_id}")
        return {"status": "paused"}
    except Exception as e:
        logger.error(f"Error pausing workflow: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/resume/{workflow_id}")
async def resume_workflow(workflow_id: str):
    try:
        logger.info(f"Resuming workflow: {workflow_id}")
        workflow_client.resume_workflow(workflow_id)
        logger.info(f"Successfully resumed workflow {workflow_id}")
        return {"status": "resumed"}
    except Exception as e:
        logger.error(f"Error resuming workflow: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory/{workflow_id}")
async def get_workflow_memory(workflow_id: str):
    try:
        logger.info(f"Getting memory for workflow: {workflow_id}")
        # Get the workflow state from Dapr state store
        state = dapr_client.get_state(
            store_name="statestore",
            key=workflow_id
        )
        if not state or not state.data:
            logger.warning(f"No memory found for workflow ID: {workflow_id}")
            raise HTTPException(status_code=404, detail="Workflow memory not found")
        logger.info(f"Retrieved memory for workflow {workflow_id}")
        return state.data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting workflow memory: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e)) 
