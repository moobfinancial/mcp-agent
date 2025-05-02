# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy dependency definitions
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Environment variables
ENV PORT=8000
ENV DATABASE_URL=postgresql://postgres:postgres@db:5432/mcp_poc

# Expose the port the app runs on
EXPOSE $PORT

# Command to run
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "${PORT}"]
