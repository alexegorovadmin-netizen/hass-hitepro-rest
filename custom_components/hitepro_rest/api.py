from __future__ import annotations

import aiohttp


class HiteProApiError(Exception):
    pass


class HiteProAuthError(HiteProApiError):
    pass


class HiteProClient:
    def __init__(self, session: aiohttp.ClientSession, base_url: str, username: str, password: str) -> None:
        self._session = session
        self._base_url = base_url.rstrip("/")
        self._auth = aiohttp.BasicAuth(username, password)

    async def async_get_devices(self) -> list[dict]:
        return await self._request("GET", "/devices/")

    async def async_get_device(self, device_id: int) -> dict:
        return await self._request("GET", f"/devices/{device_id}")

    async def async_send_command(self, device_id: int, command: int) -> dict:
        return await self._request("PUT", f"/devices/{device_id}/{command}")

    async def _request(self, method: str, path: str) -> dict:
        url = f"{self._base_url}{path}"
        try:
            async with self._session.request(
                method, url, auth=self._auth, timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status == 401:
                    raise HiteProAuthError("Invalid HiTE PRO REST API credentials")
                if resp.status != 200:
                    raise HiteProApiError(f"HiTE PRO API returned HTTP {resp.status} for {method} {path}")
                return await resp.json()
        except aiohttp.ClientError as err:
            raise HiteProApiError(f"Error communicating with HiTE PRO Gateway: {err}") from err
