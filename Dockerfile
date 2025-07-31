FROM python:3.12-slim

# Prevent uvicorn from buffering stdout
ENV PYTHONUNBUFFERED=1

# Set the working directory to /app
WORKDIR /app
ENV PYTHONPATH=/app

# Install system dependencies for psycopg2 and C compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . .

# Run the app using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
