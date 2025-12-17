from datetime import timedelta
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL, STOP_NAMES
from .amt_api import fetch_stop

_LOGGER = logging.getLogger(__name__)


def calculate_vehicle_position(target_stop, tracking_stops, all_stop_data, route, vehicle, headsign, wait_time, routes_config=None):
    """Calculate how many stops away a vehicle is from the target stop.
    
    Args:
        target_stop: The stop ID we're tracking to (e.g., "0731")
        tracking_stops: List of stop IDs in order before the target stop
        all_stop_data: Dictionary of all stop data {stop_id: {next: [...], ...}}
        route: Route number (e.g., "513")
        vehicle: Vehicle number (e.g., "0E181")
        headsign: Destination (e.g., "VIA ISONZO")
        wait_time: Wait time in minutes for this bus at the target stop
        routes_config: Dictionary with route information {route: {"stops": [...], "departure": "..."}}
    
    Returns:
        dict with position info: {"stops_away": int, "current_stop": str, "found": bool, "at_departure": bool, "scheduled_time": str}
    """
    # Get departure stop for this route
    departure_stop = None
    route_stops = None
    target_index = None  # Initialize outside conditional to avoid NameError
    if routes_config and route in routes_config:
        route_stops = routes_config[route].get("stops", [])
        departure_stop = routes_config[route].get("departure")
        if target_stop in route_stops:
            target_index = route_stops.index(target_stop)
    
    target_stop_name = STOP_NAMES.get(target_stop, target_stop)
    
    # Check tracking stops in reverse order (closest to target first)
    # Only consider a bus "at" a stop if its wait time at that stop is reasonable (< 5 minutes)
    for i, stop_id in enumerate(reversed(tracking_stops)):
        stop_data = all_stop_data.get(stop_id, {}).get("next", [])
        for bus_at_stop in stop_data:
            if (bus_at_stop.get("vehicle") == vehicle and 
                (bus_at_stop.get("route") == route or bus_at_stop.get("route") == f"{route}/") and
                bus_at_stop.get("headsign") == headsign):
                # Only consider bus as "at" this stop if wait time is reasonable (< 5 minutes)
                # This prevents showing a bus as "at stop X" when it's actually far away
                bus_wait_at_stop = bus_at_stop.get("wait", 999)
                if bus_wait_at_stop > 5:
                    continue  # Bus is too far from this stop, skip it
                
                # Check if bus is at departure stop
                if departure_stop and stop_id == departure_stop:
                    scheduled_time = bus_at_stop.get("time", "")
                    stop_name = STOP_NAMES.get(stop_id, stop_id)
                    return {"stops_away": None, "current_stop": stop_id, "current_stop_name": stop_name, "target_stop_name": target_stop_name, "found": True, "at_departure": True, "scheduled_time": scheduled_time}
                
                # Calculate stops_away using route if available, otherwise use index
                if route_stops and target_index is not None and stop_id in route_stops:
                    current_index = route_stops.index(stop_id)
                    stops_away = target_index - current_index
                    # Ensure stops_away is positive (bus should be before target)
                    if stops_away <= 0:
                        continue  # Invalid position, skip
                else:
                    stops_away = i + 1
                stop_name = STOP_NAMES.get(stop_id, stop_id)
                return {"stops_away": stops_away, "current_stop": stop_id, "current_stop_name": stop_name, "target_stop_name": target_stop_name, "found": True, "at_departure": False}
    
    # Before checking if bus is at target stop, explicitly check departure stop
    # This prevents marking a bus as "at your stop" when it's actually still at departure
    if departure_stop and departure_stop in all_stop_data:
        departure_data = all_stop_data.get(departure_stop, {}).get("next", [])
        for bus in departure_data:
            if (bus.get("vehicle") == vehicle and 
                (bus.get("route") == route or bus.get("route") == f"{route}/") and
                bus.get("headsign") == headsign):
                # Only consider at departure if wait time is reasonable
                bus_wait_at_departure = bus.get("wait", 999)
                if bus_wait_at_departure <= 10:  # Allow longer wait at departure
                    scheduled_time = bus.get("time", "")
                    stop_name = STOP_NAMES.get(departure_stop, departure_stop)
                    return {"stops_away": None, "current_stop": departure_stop, "current_stop_name": stop_name, "target_stop_name": target_stop_name, "found": True, "at_departure": True, "scheduled_time": scheduled_time}
    
    # If not found at tracking stops or departure, check if bus is actually at target stop
    # Only consider it "at your stop" if wait time is very short (≤ 1 minute) AND not at departure
    if wait_time <= 1:
        target_data = all_stop_data.get(target_stop, {}).get("next", [])
        for bus in target_data:
            if (bus.get("vehicle") == vehicle and 
                (bus.get("route") == route or bus.get("route") == f"{route}/") and
                bus.get("headsign") == headsign):
                stop_name = STOP_NAMES.get(target_stop, target_stop)
                return {"stops_away": 0, "current_stop": target_stop, "current_stop_name": stop_name, "target_stop_name": target_stop_name, "found": True, "at_departure": False}
    
    # Bus not found at tracking stops, departure, or target stop (or too far away)
    return {"stops_away": None, "current_stop": None, "current_stop_name": None, "target_stop_name": target_stop_name, "found": False, "at_departure": False}


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up AMT Genova sensors from YAML via discovery."""
    _LOGGER.info("AMT Genova: async_setup_platform called")
    stops = hass.data.get(DOMAIN, {}).get("stops", [])
    _LOGGER.info("AMT Genova: Retrieved stops from hass.data: %s", stops)

    if not stops:
        _LOGGER.warning("AMT Genova: No stops found in hass.data, skipping sensor setup")
        return

    # Get tracking stops configuration (stops to monitor for vehicle tracking)
    # Format: tracking_stops: {"0731": ["0729", "0730"], "0732": ["0729", "0730", "0731"]}
    tracking_stops_config = hass.data.get(DOMAIN, {}).get("tracking_stops", {})
    
    # Get routes configuration for accurate position calculation
    routes_config = hass.data.get(DOMAIN, {}).get("routes", {})

    async def async_update():
        """Fetch data from AMT Genova API."""
        data = {}
        
        # Fetch data for main stops
        for stop in stops:
            try:
                result = await hass.async_add_executor_job(fetch_stop, stop)
                data[stop] = result
            except Exception as err:
                _LOGGER.error("Error updating stop %s: %s", stop, err)
                data[stop] = {"next": [], "stop": stop, "updated": None}
        
        # Fetch data for tracking stops
        all_tracking_stops = set()
        for target_stop, tracking_list in tracking_stops_config.items():
            all_tracking_stops.update(tracking_list)
        
        for tracking_stop in all_tracking_stops:
            if tracking_stop not in data:  # Don't fetch if already fetched as main stop
                try:
                    result = await hass.async_add_executor_job(fetch_stop, tracking_stop)
                    data[tracking_stop] = result
                except Exception as err:
                    _LOGGER.error("Error updating tracking stop %s: %s", tracking_stop, err)
                    data[tracking_stop] = {"next": [], "stop": tracking_stop, "updated": None}
        
        # Calculate vehicle positions for each main stop
        for stop_id in stops:
            stop_data = data.get(stop_id, {})
            buses = stop_data.get("next", [])
            tracking_stops = tracking_stops_config.get(stop_id, [])
            
            for bus in buses:
                vehicle = bus.get("vehicle")
                route = bus.get("route", "").rstrip("/")
                headsign = bus.get("headsign")
                wait_time = bus.get("wait", 999)
                
                if vehicle and tracking_stops:
                    position_info = calculate_vehicle_position(
                        stop_id, tracking_stops, data, route, vehicle, headsign, wait_time, routes_config
                    )
                    bus["position"] = position_info
        
        if not data:
            raise UpdateFailed("Failed to fetch any stop data")
        return data

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="AMT Genova",
        update_method=async_update,
        update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
    )

    # For YAML setup, use async_refresh instead of async_config_entry_first_refresh
    await coordinator.async_refresh()

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