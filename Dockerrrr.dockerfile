# Use an official Python image as base
FROM python:3.9-slim
# Set working directory in container
WORKDIR /app
# Copy requirements file
COPY requirements.txt .
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy application code
COPY . .
# Expose port 5000 for WiFiNavigator API
EXPOSE 5000
# Run command to start WiFiNavigator API
CMD ["python", "app.py"]
