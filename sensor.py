"""Sensor platform for D-Link Router."""

import logging
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfDataRate,
    UnitOfInformation,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Установка сенсоров."""
    
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    sensors = [
        # CPU Load
        DLinkSensor(
            coordinator,
            "cpu_load_1",
            "CPU Load 1 min",
            None,
            None,
            SensorStateClass.MEASUREMENT,
        ),
        DLinkSensor(
            coordinator,
            "cpu_load_5",
            "CPU Load 5 min",
            None,
            None,
            SensorStateClass.MEASUREMENT,
        ),
        DLinkSensor(
            coordinator,
            "cpu_load_15",
            "CPU Load 15 min",
            None,
            None,
            SensorStateClass.MEASUREMENT,
        ),
        
        # Memory
        DLinkSensor(
            coordinator,
            "memory_percentage",
            "Memory Usage",
            PERCENTAGE,
            None,
            SensorStateClass.MEASUREMENT,
        ),
        DLinkSensor(
            coordinator,
            "memory_used",
            "Memory Used",
            UnitOfInformation.MEGABYTES,
            None,
            SensorStateClass.MEASUREMENT,
        ),
        DLinkSensor(
            coordinator,
            "memory_free",
            "Memory Free",
            UnitOfInformation.MEGABYTES,
            None,
            SensorStateClass.MEASUREMENT,
        ),
        
        # Uptime
        DLinkSensor(
            coordinator,
            "uptime",
            "Uptime",
            None,
            None,
            None,
        ),
        
        # Connected Devices
        DLinkSensor(
            coordinator,
            "connected_devices_count",
            "Connected Devices",
            "devices",
            None,
            SensorStateClass.MEASUREMENT,
        ),
    ]
    
    # Добавляем сенсоры для интерфейсов
    if coordinator.data and "interfaces" in coordinator.data:
        for iface_name in coordinator.data["interfaces"].keys():
            # RX
            sensors.append(
                DLinkInterfaceSensor(
                    coordinator,
                    iface_name,
                    "rx_bytes",
                    f"{iface_name} RX",
                    UnitOfInformation.BYTES,
                )
            )
            # TX
            sensors.append(
                DLinkInterfaceSensor(
                    coordinator,
                    iface_name,
                    "tx_bytes",
                    f"{iface_name} TX",
                    UnitOfInformation.BYTES,
                )
            )
    
    async_add_entities(sensors)


class DLinkSensor(CoordinatorEntity, SensorEntity):
    """Базовый сенсор D-Link Router."""
    
    def __init__(
        self,
        coordinator,
        data_key,
        name,
        unit,
        device_class,
        state_class,
    ):
        """Инициализация сенсора."""
        super().__init__(coordinator)
        self._data_key = data_key
        self._attr_name = f"D-Link {name}"
        self._attr_unique_id = f"dlink_router_{data_key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
    
    @property
    def native_value(self):
        """Значение сенсора."""
        if self.coordinator.data:
            return self.coordinator.data.get(self._data_key)
        return None


class DLinkInterfaceSensor(CoordinatorEntity, SensorEntity):
    """Сенсор для интерфейса."""
    
    def __init__(self, coordinator, interface, data_key, name, unit):
        """Инициализация."""
        super().__init__(coordinator)
        self._interface = interface
        self._data_key = data_key
        self._attr_name = f"D-Link {name}"
        self._attr_unique_id = f"dlink_router_{interface}_{data_key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
    
    @property
    def native_value(self):
        """Значение сенсора."""
        if self.coordinator.data and "interfaces" in self.coordinator.data:
            interfaces = self.coordinator.data["interfaces"]
            if self._interface in interfaces:
                return interfaces[self._interface].get(self._data_key)
        return None