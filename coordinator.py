"""Data coordinator for D-Link Router."""

import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant

from .api import DLinkRouterAPI
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class DLinkRouterDataUpdateCoordinator(DataUpdateCoordinator):
    """Координатор для обновления данных."""
    
    def __init__(self, hass: HomeAssistant, api: DLinkRouterAPI):
        """Инициализация."""
        self.api = api
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
    
    async def _async_update_data(self):
        """Получить данные с маршрутизатора."""
        try:
            # Выполняем в отдельном потоке (не блокируем Home Assistant)
            data = await self.hass.async_add_executor_job(
                self._get_router_data
            )
            return data
        except Exception as err:
            raise UpdateFailed(f"Ошибка обновления: {err}")
    
    def _get_router_data(self):
        """Получить данные (синхронная функция)."""
        try:
            # Подключаемся
            if not self.api.connect():
                raise ConnectionError("Не удалось подключиться к маршрутизатору")
            
            # Получаем данные
            data = self.api.get_system_info()
            
            # Отключаемся
            self.api.disconnect()
            
            _LOGGER.debug("Данные обновлены: %s", data)
            return data
            
        except Exception as err:
            # В случае ошибки всё равно отключаемся
            self.api.disconnect()
            raise