"""Safe weather data-fetching agent."""

import logging
import time
from pathlib import Path

import requests


# Create the logs directory path
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Create the log file path
LOG_FILE = LOG_DIR / "agent.log"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def fetch_weather(latitude, longitude):
    """Fetch current weather data from Open-Meteo API with retries."""
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m"
    }

    max_retries = 3

    for attempt in range(1, max_retries + 1):
        logger.info(
            "Fetching weather data from API (attempt %d/%d)",
            attempt,
            max_retries
        )

        try:
            response = requests.get(
                url,
                params=params,
                timeout=10
            )
            response.raise_for_status()

            logger.info("Weather API request successful")
            return response.json()

        except requests.RequestException as error:
            logger.error(
                "Weather API request failed on attempt %d: %s",
                attempt,
                error
            )

            if attempt < max_retries:
                logger.info("Retrying weather API request...")
                time.sleep(2)

    logger.error(
        "Weather API failed after %d attempts",
        max_retries
    )

    return None


def validate_weather(data):
    """Validate the weather API response."""
    if not isinstance(data, dict):
        logger.error(
            "Invalid weather response: expected a dictionary"
        )
        return False

    if "current" not in data:
        logger.error(
            "Invalid weather response: 'current' field missing"
        )
        return False

    current = data["current"]

    if "temperature_2m" not in current:
        logger.error(
            "Invalid weather response: temperature missing"
        )
        return False

    if "wind_speed_10m" not in current:
        logger.error(
            "Invalid weather response: wind speed missing"
        )
        return False

    logger.info("Weather data validation successful")
    return True


def make_weather_decision(temperature, wind_speed):
    """Make a simple decision based on weather conditions."""
    if temperature >= 30:
        decision = "It is hot. Stay hydrated."

    elif wind_speed >= 30:
        decision = "It is windy. Be careful outdoors."

    else:
        decision = "Weather conditions are comfortable."

    logger.info("Weather decision: %s", decision)

    return decision


def main():
    """Start and stop the weather agent."""
    logger.info("Weather Agent started")

    print("Weather Agent is running...")

    # Calicut/Kozhikode coordinates
    latitude = 11.2588
    longitude = 75.7804

    weather = fetch_weather(latitude, longitude)

    if weather and validate_weather(weather):
        temperature = weather["current"]["temperature_2m"]
        wind_speed = weather["current"]["wind_speed_10m"]

        print(f"Temperature: {temperature} °C")
        print(f"Wind Speed: {wind_speed} km/h")

        decision = make_weather_decision(
            temperature,
            wind_speed
        )

        print(f"Recommendation: {decision}")

    else:
        print("Unable to retrieve valid weather data.")
        logger.error("Weather agent could not process weather data.")

    logger.info("Weather Agent stopped")


if __name__ == "__main__":
    main()
