from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, TYPE_POWER
from .coordinator import HiteProCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: HiteProCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        HiteProPowerSensor(coordinator, device_id)
        for device_id, device in coordinator.data.items()
        if device.get("type") == TYPE_POWER
    )


class HiteProPowerSensor(CoordinatorEntity[HiteProCoordinator], BinarySensorEntity):
    _attr_has_entity_name = True
    _attr_device_class = BinarySensorDeviceClass.POWER

    def __init__(self, coordinator: HiteProCoordinator, device_id: int) -> None:
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_unique_id = f"hitepro_rest_power_{device_id}"
        self._attr_name = coordinator.data[device_id]["name"].strip()

    @property
    def is_on(self) -> bool | None:
        device = self.coordinator.data.get(self._device_id)
        if device is None:
            return None
        return bool(device["status"])

    @property
    def available(self) -> bool:
        return super().available and self._device_id in self.coordinator.data
