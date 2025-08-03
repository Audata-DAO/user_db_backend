FROM python:3.12-slim

# Set the working directory to /app
WORKDIR /app

# Copy and install Python dependencies
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the project
COPY . /app/

# Run the app using uvicorn
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
