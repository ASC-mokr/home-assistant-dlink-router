"""Binary sensor platform for D-Link Router."""

import logging
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Установка бинарных сенсоров."""
    
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    sensors = [
        DLinkConnectivitySensor(coordinator),
    ]
    
    async_add_entities(sensors)


class DLinkConnectivitySensor(CoordinatorEntity, BinarySensorEntity):
    """Сенсор подключения к маршрутизатору."""
    
    def __init__(self, coordinator):
        """Инициализация."""
        super().__init__(coordinator)
        self._attr_name = "D-Link Router Connection"
        self._attr_unique_id = "dlink_router_connection"
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    
    @property
    def is_on(self):
        """Подключён ли маршрутизатор."""
        return self.coordinator.last_update_success