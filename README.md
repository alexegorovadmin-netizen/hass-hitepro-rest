# HiTE PRO (REST API) для Home Assistant

Интеграция HiTE PRO Gateway через официальный REST API (см. `api.pdf` в настройках
приложения HiTE PRO → Интеграции → Rest API → (i)), а не через MQTT/Wiren Board мост.
Причина: часть устройств не репортит состояние через MQTT-мост HiTE PRO, но исправно
работает через официальный REST API.

Поддерживаемые типы устройств (только то, что реально есть в `GET /rest/devices/`):

- `switch` — реле → HA `switch`
- `power` — датчик наличия напряжения → HA `binary_sensor` (device_class: power)
- `temperature` — датчик температуры → HA `sensor`

Типы `yandex` (сценарии Яндекса) и `transmitter` (кнопки, требуют webhook) — вне
объёма первой версии: их поведение по команде не описано в официальной документации.

## Установка

HACS → Integrations → ⋮ → Custom repositories → добавить URL этого репозитория как
Integration → найти "HiTE PRO (REST API)" → Download → перезапустить Home Assistant.

## Настройка

Settings → Devices & Services → Add Integration → "HiTE PRO (REST API)":

- **Base URL**: `http://hitepro.local/rest` (в локальной сети) или
  `https://<внешний ключ>.connect-profi.ru/rest` (внешний, ключ — в приложении HiTE PRO,
  Настройки → об устройстве)
- **Логин**: email/телефон аккаунта HiTE PRO
- **Пароль**: пароль REST API (приложение HiTE PRO → Интеграции → Rest API →
  «Сбросить пароль» — показывается один раз)
