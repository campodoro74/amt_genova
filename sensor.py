from datetime import timedelta
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .amt_api import fetch_stop

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up AMT Genova sensors from YAML via discovery."""
    stops = hass.data.get(DOMAIN, {}).get("stops", [])

    if not stops:
        return

    async def async_update():
        """Fetch data from AMT Genova API."""
        data = {}
        for stop in stops:
            try:
                result = await hass.async_add_executor_job(fetch_stop, stop)
                data[stop] = result
            except Exception as err:
                _LOGGER.error("Error updating stop %s: %s", stop, err)
                data[stop] = {"next": [], "stop": stop, "updated": None}
        if not data:
            raise UpdateFailed("Failed to fetch any stop data")
        return data

    coordinator = DataUpdateCoordinator(
        hass,
        name="AMT Genova",
        update_method=async_update,
        update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        AMTStopSensor(coordinator, stop)
        for stop in stops
    )


class AMTStopSensor(SensorEntity):
    """Sensor providing next departure wait time for an AMT stop."""

    def __init__(self, coordinator, stop_id):
        self.coordinator = coordinator
        self.stop_id = stop_id
        self._attr_name = f"AMT {stop_id}"
        self._attr_unique_id = f"amt_{stop_id}"

    @property
    def should_poll(self):
        """No need to poll, coordinator handles it."""
        return False

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.last_update_success

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        data = self.coordinator.data.get(self.stop_id, {})
        nxt = data.get("next", [])
        return nxt[0]["wait"] if nxt else None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
        return self.coordinator.data.get(self.stop_id, {})

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update the entity."""
        await self.coordinator.async_request_refresh()


