"""Climate platform for Midea AC LAN integration."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

try:
    from msmart.device import air_conditioning as ac
    from msmart.device import device as midea_device
except ImportError:
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.error("msmart library not installed. Run: pip install msmart")
    ac = None
    midea_device = None

_LOGGER = logging.getLogger(__name__)

HVAC_MODES = [HVACMode.OFF, HVACMode.COOL, HVACMode.HEAT, HVACMode.AUTO, HVACMode.FAN_ONLY]
FAN_MODES = ["auto", "low", "medium", "high"]


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Midea AC LAN climate entities."""
    if ac is None:
        _LOGGER.error("msmart library not available. Cannot set up Midea AC LAN.")
        return

    data = config_entry.data
    device = MideaACDevice(
        hass=hass,
        host=data["host"],
        device_id=data["id"],
        token=data["token"],
        key=data["key"],
        port=data.get("port", 6444),
        name=data.get("name", f"Midea AC {data['host']}"),
    )
    
    async_add_entities([MideaACClimate(device, config_entry.entry_id)])


class MideaACDevice:
    """Representation of a Midea AC device."""

    def __init__(self, hass: HomeAssistant, host: str, device_id: int, token: str, key: str, port: int = 6444, name: str = ""):
        """Initialize the device."""
        self.hass = hass
        self.host = host
        self.device_id = device_id
        self.token = token
        self.key = key
        self.port = port
        self.name = name
        self._device = None
        self._lock = asyncio.Lock()

    async def _get_device(self):
        """Get or create the device connection."""
        if self._device is None:
            self._device = ac(self.host, self.device_id, self.port)
            self._device.set_token(self.token)
            self._device.set_key(self.key)
        return self._device

    async def refresh(self):
        """Refresh device state."""
        async with self._lock:
            device = await self._get_device()
            await self.hass.async_add_executor_job(device.refresh)

    async def apply(self):
        """Apply current settings to device."""
        async with self._lock:
            device = await self._get_device()
            await self.hass.async_add_executor_job(device.apply)


class MideaACClimate(ClimateEntity):
    """Representation of a Midea AC climate entity."""

    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.FAN_MODE
        | ClimateEntityFeature.SWING_MODE
    )

    def __init__(self, device: MideaACDevice, entry_id: str):
        """Initialize the climate entity."""
        self._device = device
        self._entry_id = entry_id
        self._attr_unique_id = f"midea_ac_lan_{device.device_id}"
        self._attr_name = device.name or f"Midea AC {device.host}"

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        if self._device._device:
            return self._device._device.indoor_temperature
        return None

    @property
    def target_temperature(self) -> float | None:
        """Return the target temperature."""
        if self._device._device:
            return self._device._device.target_temperature
        return None

    @property
    def hvac_mode(self) -> HVACMode:
        """Return current HVAC mode."""
        if not self._device._device or not self._device._device.power_state:
            return HVACMode.OFF
        
        mode_map = {
            1: HVACMode.COOL,
            2: HVACMode.HEAT,
            3: HVACMode.AUTO,
            4: HVACMode.FAN_ONLY,
        }
        return mode_map.get(self._device._device.operational_mode, HVACMode.AUTO)

    @property
    def hvac_modes(self) -> list[HVACMode]:
        """Return the list of available HVAC modes."""
        return HVAC_MODES

    @property
    def fan_mode(self) -> str | None:
        """Return the fan mode."""
        if self._device._device:
            fan_map = {0: "auto", 1: "low", 2: "medium", 3: "high"}
            return fan_map.get(self._device._device.fan_speed, "auto")
        return None

    @property
    def fan_modes(self) -> list[str]:
        """Return the list of available fan modes."""
        return FAN_MODES

    async def async_update(self) -> None:
        """Update the device state."""
        await self._device.refresh()

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        if ATTR_TEMPERATURE in kwargs:
            if self._device._device:
                self._device._device.target_temperature = kwargs[ATTR_TEMPERATURE]
                await self._device.apply()
                await self.async_update()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target HVAC mode."""
        if self._device._device:
            if hvac_mode == HVACMode.OFF:
                self._device._device.power_state = False
            else:
                self._device._device.power_state = True
                mode_map = {
                    HVACMode.COOL: 1,
                    HVACMode.HEAT: 2,
                    HVACMode.AUTO: 3,
                    HVACMode.FAN_ONLY: 4,
                }
                self._device._device.operational_mode = mode_map.get(hvac_mode, 3)
            await self._device.apply()
            await self.async_update()

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        """Set new target fan mode."""
        if self._device._device:
            fan_map = {"auto": 0, "low": 1, "medium": 2, "high": 3}
            self._device._device.fan_speed = fan_map.get(fan_mode, 0)
            await self._device.apply()
            await self.async_update()

