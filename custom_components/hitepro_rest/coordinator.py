from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import HiteProApiError, HiteProClient
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class HiteProCoordinator(DataUpdateCoordinator[dict[int, dict]]):
    def __init__(self, hass: HomeAssistant, client: HiteProClient) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.client = client

    async def _async_update_data(self) -> dict[int, dict]:
        try:
            devices = await self.client.async_get_devices()
        except HiteProApiError as err:
            raise UpdateFailed(str(err)) from err
        return {device["id"]: device for device in devices}
