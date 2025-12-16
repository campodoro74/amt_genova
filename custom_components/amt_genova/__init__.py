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

<<<<<<< Updated upstream
=======

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AMT Genova from a config entry.
    
    This integration is YAML-only. If a config entry exists, we raise ConfigEntryError
    before forwarding to prevent Home Assistant from trying to load it as a config entry.
    """
    from homeassistant.exceptions import ConfigEntryError
    
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

>>>>>>> Stashed changes
