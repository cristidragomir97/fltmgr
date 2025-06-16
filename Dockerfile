FROM python:3.11-slim

# System deps
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy code
COPY . /app

# Install Python deps
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Default port
EXPOSE 8000

# Run API server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
