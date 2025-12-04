# Build Stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final Stage
FROM python:3.11-slim
WORKDIR /app
ENV TZ=UTC

# System Deps
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copy Artifacts
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

# Configure Cron
COPY scheduler/cron-task /etc/cron.d/cron-task
RUN chmod 0644 /etc/cron.d/cron-task && crontab /etc/cron.d/cron-task
RUN mkdir -p /data /cron

# Launch
# Note: "src.server:api" refers to src/server.py and the "api = FastAPI()" object
CMD cron && uvicorn src.server:api --host 0.0.0.0 --port 8080