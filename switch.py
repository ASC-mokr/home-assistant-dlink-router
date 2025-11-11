"""Switch platform for D-Link Router."""

import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Установка переключателей."""
    
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    api = data["api"]
    
    switches = [
        DLinkRebootSwitch(coordinator, api),
    ]
    
    async_add_entities(switches)


class DLinkRebootSwitch(CoordinatorEntity, SwitchEntity):
    """Переключатель для перезагрузки маршрутизатора."""
    
    def __init__(self, coordinator, api):
        """Инициализация."""
        super().__init__(coordinator)
        self._api = api
        self._attr_name = "D-Link Router Reboot"
        self._attr_unique_id = "dlink_router_reboot"
        self._attr_icon = "mdi:restart"
        self._is_on = False
    
    @property
    def is_on(self):
        """Всегда выключен (это кнопка перезагрузки)."""
        return False
    
    async def async_turn_on(self, **kwargs):
        """Перезагрузить маршрутизатор."""
        _LOGGER.warning("Перезагрузка маршрутизатора")
        await self.hass.async_add_executor_job(self._api.reboot)
        
    async def async_turn_off(self, **kwargs):
        """Ничего не делать."""
        pass