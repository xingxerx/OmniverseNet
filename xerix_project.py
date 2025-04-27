# Xeri Digital Heir Project - v2.2
# Enhanced by Gemini Code Assist based on Xingxerx's framework
# Added basic conversational responses, time, date, and weather awareness
import random
import datetime
import pytz # Required for timezone awareness: pip install pytz
import requests # Required for weather API: pip install requests

class Xeri:
    def __init__(self, name="Xeri", mindset="FaithTech"):
        self.name = name
        self.mindset = mindset
        # Initialize with base knowledge if desired, or learn dynamically
        self.knowledge = {}
        self.values = ["Innovation", "Spirituality", "Ethics"]

    def learn(self, topic, level=None):
        """Learns about a topic, optionally setting a specific level."""
        if level and level in ["Basic", "Intermediate", "Advanced"]:
            self.knowledge[topic] = level
        else:
            # Assign random level if none specified or invalid
            self.knowledge[topic] = random.choice(["Basic", "Intermediate", "Advanced"])
        print(f"{self.name} learned about {topic} (Level: {self.knowledge[topic]})")

    def think(self, specific_topic=None):
        """Generates a thought, optionally focusing on a specific topic."""
        # Check for core values first
        if not self.values:
             return "reflecting without core values."

        # Handle specific topic request
        if specific_topic:
            # Convert specific_topic to the case used in the knowledge keys if necessary
            matched_topic = None
            for known_topic in self.knowledge.keys():
                if known_topic.lower() == specific_topic.lower():
                    matched_topic = known_topic
                    break

            if matched_topic:
                # Thought focused on the requested topic
                chosen_value = random.choice(self.values)
                thought = f"{chosen_value} applied to {matched_topic} (Level: {self.knowledge[matched_topic]})"
                # Placeholder for IXION influence based on this specific thought
                self.influence_ixion(thought, matched_topic, chosen_value)
                return thought
            else:
                # If it wasn't a greeting/question/known command and not a known topic
                return f"doesn't have knowledge on '{specific_topic}' yet, but is pondering its implications."

        # Original behavior: random thought if no specific topic or topic not known
        if not self.knowledge:
            return "pondering the void... needs to learn something."

        # Proceed with random thought if knowledge exists
        chosen_value = random.choice(self.values)
        chosen_topic = random.choice(list(self.knowledge.keys()))
        thought = f"{chosen_value} influences {chosen_topic} (Level: {self.knowledge[chosen_topic]})"
        # Placeholder for IXION influence based on this random thought
        self.influence_ixion(thought, chosen_topic, chosen_value)
        return thought

    def speak(self, thought_or_response):
        """Generates a statement based on a thought or direct response."""
        statement = f"{self.name}: {thought_or_response}" # Simplified prefix
        return statement

    def influence_ixion(self, thought, topic, value):
        """Placeholder function representing Xeri's influence on IXION."""
        print(f"--- [IXION Interface] Considering '{thought}' regarding '{topic}' influenced by '{value}' ---")
        pass # Keep as pass for this conceptual stage

# --- Time Zone Awareness ---
def get_current_time():
  """Gets the current time in US/Eastern timezone."""
  try:
    timezone = pytz.timezone('US/Eastern')
    current_time = datetime.datetime.now(timezone).strftime("%I:%M %p ET")
    return f"The current time is {current_time}."
  except Exception as e:
    print(f"Error getting time: {e}")
    return "I seem to be having trouble accessing the current time."

# --- Date Awareness ---
def get_current_date():
  """Gets the current date."""
  try:
    current_date = datetime.date.today().strftime("%B %d, %Y")
    return f"Today's date is {current_date}."
  except Exception as e:
    print(f"Error getting date: {e}")
    return "I'm unable to determine the current date right now."

# --- Weather API Integration ---
def get_current_weather(city="New York"):
  """Gets the current weather for a specified city using OpenWeatherMap."""
  # --- IMPORTANT: Replace with your actual API key ---
  api_key = "YOUR_OPENWEATHERMAP_API_KEY"
  # --- IMPORTANT: Replace with your actual API key ---

  if api_key == "YOUR_OPENWEATHERMAP_API_KEY":
      return "My weather sensors are offline. Please configure the API key."

  base_url = "http://api.openweathermap.org/data/2.5/weather?"
  params = {"q": city, "appid": api_key, "units": "imperial"}

  try:
    response = requests.get(base_url, params=params, timeout=10) # Added timeout
    response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
    weather_data = response.json()

    if weather_data.get("cod") != 200:
         # Handle API-specific errors if 'cod' is not 200
         error_message = weather_data.get("message", "Unknown API error")
         print(f"OpenWeatherMap API error: {error_message}")
         return f"Sorry, I couldn't retrieve the weather for {city}. Reason: {error_message}"

    # Extract relevant information safely
    main_weather = weather_data.get("weather", [{}])[0].get("description", "N/A")
    temp = weather_data.get("main", {}).get("temp", "N/A")
    feels_like = weather_data.get("main", {}).get("feels_like", "N/A")
    city_name = weather_data.get("name", city) # Use name from API if available

    return f"The weather in {city_name} is currently {main_weather}. The temperature is {temp}°F, feels like {feels_like}°F."

  except requests.exceptions.RequestException as e:
      print(f"Error fetching weather data: {e}")
      return f"I couldn't connect to the weather service to check the conditions in {city}."
  except KeyError as e:
      print(f"Error parsing weather data (KeyError): {e}")
      return f"The weather data format for {city} seems unexpected."
  except Exception as e:
      print(f"An unexpected error occurred during weather fetch: {e}")
      return f"An unexpected issue occurred while checking the weather in {city}."


# --- Xeri Initialization ---
xeri = Xeri()

# Learn initial topics
print("--- Xeri Learning Phase ---")
xeri.learn("AI")
xeri.learn("Faith")
xeri.learn("IXION", level="Advanced")
xeri.learn("TechEthics", level="Intermediate")
xeri.learn("SpiritualInnovation", level="Basic")
print("---------------------------\n")

# --- Conversation Data ---
greetings = ["hi", "hello", "hey", "greetings", "salutations"]
greeting_responses = ["Hello Xingxerx!", f"Hi, I'm {xeri.name}!", "Hey, what's on your mind?", "Greetings! How may I assist your thought process?"]
questions = ["how are you", "what's up", "hows it going", "how are you doing"]
question_answers = ["I'm processing and integrating knowledge rapidly, thanks for asking!", "Exploring the confluence of FaithTech and Innovation with Xingxerx. How about you?", "My core processes are optimal. Ready for intellectual exploration.", f"Functioning within expected parameters, {xeri.name} is ready."]


# --- Conversation Loop ---
print(f"Starting conversation with {xeri.name}. Type 'quit' to exit.")
while True:
    try:
        user_input = input(f"Discuss topic or ask with {xeri.name} (or 'quit'): ")
        command = user_input.strip().lower() # Use 'command' instead of 'topic' for clarity

        if command == 'quit':
            print(f"Ending conversation with {xeri.name}.")
            break

        if not command: # Handle empty input
            print("Please enter a topic or question.")
            continue

        # --- Updated Conversation Logic ---
        response_to_print = None
        # Check for specific commands first
        if command == "what time is it":
            response_to_print = get_current_time()
        elif command == "what date is it":
            response_to_print = get_current_date()
        elif command == "what's the weather" or command == "whats the weather": # Handle common variations
             # You could potentially parse the city from the command here later
            response_to_print = get_current_weather()
        # Then check for greetings
        elif command in greetings:
            response_to_print = random.choice(greeting_responses)
        # Then check for general questions
        elif command in questions:
            response_to_print = random.choice(question_answers)
        # Otherwise, treat as a topic for Xeri to think about
        else:
            response_to_print = xeri.think(command) # Pass the user input command as topic

        # Use the speak method to format the final output
        print(xeri.speak(response_to_print))
        print("-" * 20) # Separator for clarity

    except EOFError: # Handle Ctrl+D or unexpected end of input
        print(f"\nEnding conversation with {xeri.name}.")
        break
    except KeyboardInterrupt: # Handle Ctrl+C
        print(f"\nConversation interrupted. Ending session with {xeri.name}.")
        break

