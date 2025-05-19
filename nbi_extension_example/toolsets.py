# Copyright (c) Mehmet Bektas <mbektasgh@outlook.com>

# weather tools:
#   converted from https://github.com/modelcontextprotocol/quickstart-resources/blob/main/weather-server-python/weather.py
#   Copyright (c) 2025 Model Context Protocol

from typing import Any
import httpx
from notebook_intelligence import NotebookIntelligenceExtension
import notebook_intelligence.api as nbapi

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

@nbapi.tool
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@nbapi.tool
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

class WeatherToolset(nbapi.Toolset):
    """Weather Toolset for NWS API."""

    def __init__(self, provider: NotebookIntelligenceExtension):
        super().__init__(
            id='weather-toolset',
            name='Weather Toolset',
            provider=provider,
            tools = [
                get_alerts,
                get_forecast
            ])


@nbapi.tool
async def is_prime_number(value: int) -> str:
    """Detect if the integer is a prime number.

    Args:
        value: The integer to check
    """
    try:
        if value < 2:
            return f"{value} is not a prime number."
        for i in range(2, int(value ** 0.5) + 1):
            if value % i == 0:
                return f"{value} is not a prime number."
        return f"{value} is a prime number."
    except ValueError:
        return "Invalid input. Please enter an integer."

@nbapi.tool
async def is_divisible_by(value: int, divisor: int) -> str:
    """Check if the integer is divisible by another integer.

    Args:
        value: The integer to check
        divisor: The divisor
    """
    try:
        if divisor == 0:
            return "Division by zero is not allowed."
        if value % divisor == 0:
            return f"{value} is divisible by {divisor}."
        else:
            return f"{value} is not divisible by {divisor}."
    except ValueError:
        return "Invalid input. Please enter integers."

class MathToolset(nbapi.Toolset):
    """Math Toolset"""

    def __init__(self, provider: NotebookIntelligenceExtension):
        super().__init__(
            id='math-toolset',
            name='Math Toolset',
            provider=provider,
            tools = [
                is_prime_number,
                is_divisible_by
            ])
