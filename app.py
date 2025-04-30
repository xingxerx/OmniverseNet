# e:\OmniverseNet\app.py
from WiFiNavigator import WiFiNavigator
app = Flask(__name__) # <-- Flask app defined here
wifi_navigator = WiFiNavigator()
@app.route('/location', methods=['GET'])
def get_location():
    return wifi_navigator.get_current_location()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # <-- Flask app runs here
