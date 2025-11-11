"""D-Link Router integration for Home Assistant."""

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD

from .api import DLinkRouterAPI
from .coordinator import DLinkRouterDataUpdateCoordinator
from .const import DOMAIN, PLATFORMS, CONF_SSH_PORT, DEFAULT_PORT

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Установка интеграции из конфига."""
    
    # Получаем параметры подключения
    host = entry.data[CONF_HOST]
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    port = entry.data.get(CONF_SSH_PORT, DEFAULT_PORT)
    
    # Создаём API объект
    api = DLinkRouterAPI(host, username, password, port)
    
    # Создаём координатор
    coordinator = DLinkRouterDataUpdateCoordinator(hass, api)
    
    # Первое обновление данных
    await coordinator.async_config_entry_first_refresh()
    
    # Сохраняем в hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "api": api,
    }
    
    # Загружаем платформы (sensor, switch и т.д.)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    _LOGGER.info("D-Link Router интеграция загружена для %s", host)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Выгрузка интеграции."""
    
    # Выгружаем платформы
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        # Отключаемся от маршрутизатора
        data = hass.data[DOMAIN].pop(entry.entry_id)
        api = data["api"]
        await hass.async_add_executor_job(api.disconnect)
    
    return unload_ok