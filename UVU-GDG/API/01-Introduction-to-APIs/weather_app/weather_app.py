# Weather Application using OpenWeatherMap API
# --------------------------------------------
# This script is a basic weather application that retrieves current weather data for a specified city.
# It demonstrates how to interact with an external API using Python, focusing on making HTTP requests,
# handling JSON responses, and extracting specific information.
# The script uses the OpenWeatherMap API to provide temperature in both Celsius and Fahrenheit,
# along with a brief weather description.

# Import the 'requests' library, which is required to send HTTP requests to the API.
import requests

# Define the 'get_weather' function, which fetches weather data.
# Parameters:
# 1. 'city_name': The city for which to retrieve weather information.
# 2. 'api_key': The OpenWeatherMap API key for authentication.
def get_weather(city_name, api_key):
    
    # Base URL for the OpenWeatherMap API.
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    # Parameters for the API request with metric units (Celsius).
    params_metric = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'
    }

    # Parameters for the API request with imperial units (Fahrenheit).
    params_imperial = {
        'q': city_name,
        'appid': api_key,
        'units': 'imperial'
    }

    # Send GET requests to the API with both metric and imperial units.
    response_metric = requests.get(base_url, params=params_metric)
    response_imperial = requests.get(base_url, params=params_imperial)

    if response_metric.status_code == 200 and response_imperial.status_code == 200:
        # Convert the API responses from JSON format to Python dictionaries.
        data_metric = response_metric.json()
        data_imperial = response_imperial.json()
        
        # Extract relevant information from the responses:
        main_metric = data_metric['main']
        weather = data_metric['weather'][0]
        main_imperial = data_imperial['main']

        # Output the city name, temperature in both Celsius and Fahrenheit, and weather description.
        print(f"City: {city_name}")
        print(f"Temperature: {main_metric['temp']}°C / {main_imperial['temp']}°F")
        print(f"Weather: {weather['description'].capitalize()}")  # Capitalize the first letter of the description.
    
    # If the requests were not successful, inform the user.
    else:
        print("City not found or API request failed. Please try again.")

# Main execution block.
# Prompts the user for the API key and city name, then calls 'get_weather'.
if __name__ == "__main__":
    # Use the API key from your OpenWeatherMap account
    api_key = "fe5acf716b01bbdf49e0d23b12ac8921"
    
    # Prompt the user to enter the city name.
    city_name = input("Enter city name: ")
    
    # Fetch and display the weather data.
    get_weather(city_name, api_key)