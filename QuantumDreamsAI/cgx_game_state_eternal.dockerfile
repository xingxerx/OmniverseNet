FROM python:3.9
# Set working directory
WORKDIR /app
# Copy requirements file
COPY requirements.txt .
# Install dependencies
RUN pip install -r requirements.txt
# Copy game state files
COPY game_state.py .
COPY nexus_explorer.py .
COPY multiverse_sdk .
COPY erebus_ai .
# Expose port for potential future online play
EXPOSE 8080
# Run game state command
CMD ["python", "game_state.py"]

