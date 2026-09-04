from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, TYPE_TEMPERATURE
from .coordinator import HiteProCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: HiteProCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        HiteProTemperatureSensor(coordinator, device_id)
        for device_id, device in coordinator.data.items()
        if device.get("type") == TYPE_TEMPERATURE
    )


class HiteProTemperatureSensor(CoordinatorEntity[HiteProCoordinator], SensorEntity):
    _attr_has_entity_name = True
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, coordinator: HiteProCoordinator, device_id: int) -> None:
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_unique_id = f"hitepro_rest_temperature_{device_id}"
        self._attr_name = coordinator.data[device_id]["name"].strip()

    @property
    def native_value(self) -> float | None:
        device = self.coordinator.data.get(self._device_id)
        if device is None:
            return None
        return device["status"]

    @property
    def available(self) -> bool:
        return super().available and self._device_id in self.coordinator.data
