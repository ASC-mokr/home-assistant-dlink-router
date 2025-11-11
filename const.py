"""Constants for D-Link Router integration."""

# Имя домена (не меняйте!)
DOMAIN = "dlink_router"
NAME = "D-Link Router"

# Значения по умолчанию
DEFAULT_NAME = "D-Link DIR-825"
DEFAULT_HOST = "192.168.1.100"
DEFAULT_PORT = 22
DEFAULT_USERNAME = "admin"
DEFAULT_SCAN_INTERVAL = 30  # секунды (обновление каждые 30 секунд)

# Платформы (типы устройств)
PLATFORMS = ["sensor", "switch", "binary_sensor"]

# Конфигурационные ключи
CONF_SSH_PORT = "ssh_port"