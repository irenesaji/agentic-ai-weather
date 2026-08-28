# Safe Data-Fetching Weather Agent

A production-ready Python weather agent built to demonstrate reliability principles for safe data fetching.

## Features

- Fetches current weather data from the Open-Meteo API
- Validates the API response before using the data
- Makes a simple weather-based decision
- Handles API failures with automatic retries
- Uses a 10-second API timeout
- Logs important actions and decisions
- Logs to both the console and a file
- Passes Pylint quality checks

## Project Structure

```text
agentic-ai-weather/
├── src/
│   └── agent.py
├── logs/
│   └── agent.log
├── .gitignore
├── requirements.txt
└── README.md