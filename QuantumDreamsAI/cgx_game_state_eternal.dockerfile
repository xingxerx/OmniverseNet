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
COPY mv_sdk.py .       # Assuming this is the correct SDK file
COPY erebus_ai.py .    # Assuming this is the correct AI file
# Expose port for potential future online play
EXPOSE 8080
# Run game state command
CMD ["python", "game_state.py"]
