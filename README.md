# Distributed LLM Agent with Dapr Workflows

This project implements a distributed LLM agent using Dapr workflows. The agent can be controlled through HTTP endpoints, allowing you to start, pause, resume, and monitor its execution.

## Prerequisites

- Python 3.8+
- Dapr CLI
- OpenAI API key

## Setup

1. Install Dapr CLI and initialize Dapr:
```bash
dapr init
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export OPENAI_API_KEY=your_api_key
```

## Running the Application

1. Start the application:
```bash
python src/main.py
```

2. The application will be available at `http://localhost:8000`

## API Endpoints

- `POST /start`: Start a new agent workflow
  - Body: JSON input for the agent
  - Returns: workflow_id

- `GET /status/{workflow_id}`: Get workflow status

- `POST /pause/{workflow_id}`: Pause workflow execution

- `POST /resume/{workflow_id}`: Resume paused workflow

- `GET /memory/{workflow_id}`: Get agent's current memory state

## Example Usage

1. Start a new workflow:
```bash
curl -X POST http://localhost:8000/start \
  -H "Content-Type: application/json" \
  -d '{"task": "Your task description"}'
```

2. Check workflow status:
```bash
curl http://localhost:8000/status/{workflow_id}
```

3. Get agent memory:
```bash
curl http://localhost:8000/memory/{workflow_id}
``` 