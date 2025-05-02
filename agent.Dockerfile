# Agent Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy dependency definitions
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Environment variables are expected to be provided at runtime
# particularly OPENAI_API_KEY and MCP_SERVER_URL

# Command to run
CMD ["python", "agent/agent_script.py"]
