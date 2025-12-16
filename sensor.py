from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .amt_api import fetch_stop


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up AMT Genova sensors from YAML via discovery."""
    stops = hass.data.get(DOMAIN, {}).get("stops", [])

    if not stops:
        return

    async def async_update():
        data = {}
        for stop in stops:
            result = await hass.async_add_executor_job(fetch_stop, stop)
            data[stop] = result
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
    def native_value(self):
        data = self.coordinator.data.get(self.stop_id, {})
        nxt = data.get("next", [])
        return nxt[0]["wait"] if nxt else None

    @property
    def extra_state_attributes(self):
        return self.coordinator.data.get(self.stop_id, {})

    async def async_update(self):
        await self.coordinator.async_request_refresh()


