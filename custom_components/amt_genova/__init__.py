from homeassistant.core import HomeAssistant
from homeassistant.helpers.discovery import async_load_platform

from .const import DOMAIN


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the AMT Genova integration from YAML."""
    stops = config.get(DOMAIN)

    # Allow configuration to be optional
    if not stops:
        return True

    # Store configuration so the sensor platform can access it
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["stops"] = stops

    # Load the sensor platform
    hass.async_create_task(
        async_load_platform(hass, "sensor", DOMAIN, {}, config)
    )

    return True

