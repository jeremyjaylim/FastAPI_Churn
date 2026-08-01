# lab-10/Dockerfile
FROM python:3.12-slim
WORKDIR /app
# Install uv for fast dependency management
RUN pip install uv
# Copy dependency files first (Docker caches this layer)
COPY pyproject.toml .
RUN uv sync --no-dev
# Copy the application code
COPY main.py .
# Expose the port FastAPI listens on
EXPOSE 8000
# Start the API server
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]