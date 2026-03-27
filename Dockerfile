# learnt setup using AI

# Use a lightweight, official Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code and data
COPY . .

# Expose the port that FastAPI runs on
EXPOSE 8000

# Run the Uvicorn web server, binding it to all network interfaces (0.0.0.0)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]