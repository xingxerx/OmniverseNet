FROM python:3.9
# Set working directory
WORKDIR /app
# Copy requirements file
COPY requirements.txt .
# Install dependencies (use cache unless requirements.txt changes)
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application code
# Using COPY . . assumes you have a good .dockerignore file
# to avoid copying unnecessary files (.venv, .git, etc.)
COPY . .

# Expose port for potential future online play
EXPOSE 8080
# Run game state command
CMD ["python", "game_state.py"]
