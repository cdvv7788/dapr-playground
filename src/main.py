import uvicorn
import logging
import logging.config
import yaml
import os
from dapr.ext.workflow import WorkflowRuntime
from workflows.agent_workflow import agent_workflow
from activities.agent import reasoning_activity, action_activity
from activities.state import save_state, get_state
from api.main import app

# Set up logging
log_config_path = os.path.join(os.path.dirname(__file__), 'logging.yaml')
with open(log_config_path, 'r') as f:
    log_config = yaml.safe_load(f)
logging.config.dictConfig(log_config)

logger = logging.getLogger(__name__)

# Register workflow and activities
workflow_runtime = WorkflowRuntime()
workflow_runtime.register_workflow(agent_workflow)
workflow_runtime.register_activity(reasoning_activity)
workflow_runtime.register_activity(action_activity)
workflow_runtime.register_activity(save_state)
workflow_runtime.register_activity(get_state)
if __name__ == "__main__":
    try:
        logger.info("Starting workflow runtime...")
        # Start the workflow runtime
        workflow_runtime.start()
        
        logger.info("Starting FastAPI application...")
        # Start the FastAPI application
        uvicorn.run(app, host="0.0.0.0", port=8000, log_config=log_config)
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}", exc_info=True)
        raise 
