"""AMT Genova integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.exceptions import ConfigEntryError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the AMT Genova integration from YAML."""
    _LOGGER.info("AMT Genova: async_setup called")
    
    amt_config = config.get(DOMAIN)
    
    # Support both simple list format and dict format
    if isinstance(amt_config, list):
        stops = amt_config
        tracking_stops = {}
        routes = {}
    elif isinstance(amt_config, dict):
        stops = amt_config.get("stops", [])
        tracking_stops = amt_config.get("tracking_stops", {})
        routes = amt_config.get("routes", {})
    else:
        stops = None
        tracking_stops = {}
        routes = {}
    
    _LOGGER.info("AMT Genova: stops from config: %s", stops)
    _LOGGER.info("AMT Genova: tracking_stops from config: %s", tracking_stops)
    _LOGGER.info("AMT Genova: routes from config: %s", routes)

    # Allow configuration to be optional
    if not stops:
        _LOGGER.warning("AMT Genova: No stops configured")
        return True

    # Store configuration so the sensor platform can access it
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["stops"] = stops
    hass.data[DOMAIN]["tracking_stops"] = tracking_stops
    hass.data[DOMAIN]["routes"] = routes
    _LOGGER.info("AMT Genova: Stored stops in hass.data: %s", stops)
    _LOGGER.info("AMT Genova: Stored tracking_stops in hass.data: %s", tracking_stops)
    _LOGGER.info("AMT Genova: Stored routes in hass.data: %s", routes)

    # Load the sensor platform
    _LOGGER.info("AMT Genova: Loading sensor platform")
    hass.async_create_task(
        async_load_platform(hass, "sensor", DOMAIN, {}, config)
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AMT Genova from a config entry.
    
    This integration is YAML-only. If a config entry exists, we raise ConfigEntryError
    before forwarding to prevent Home Assistant from trying to load it as a config entry.
    """
    _LOGGER.warning(
        "AMT Genova: Config entry detected (entry_id: %s) but integration is YAML-only. "
        "No entities will be created from this entry. Configure via configuration.yaml instead.",
        entry.entry_id
    )
    
    # Raise ConfigEntryError BEFORE forwarding, as Home Assistant requires
    # This prevents the entry from being loaded while allowing YAML to work
    raise ConfigEntryError(
        "AMT Genova is a YAML-only integration. "
        "Please configure it via configuration.yaml and remove this config entry."
    )


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, [Platform.SENSOR])
