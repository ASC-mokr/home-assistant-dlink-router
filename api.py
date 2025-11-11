"""API for D-Link Router via SSH."""

import logging
import paramiko
import re
from typing import Dict, List

_LOGGER = logging.getLogger(__name__)


class DLinkRouterAPI:
    """Класс для работы с D-Link маршрутизатором через SSH."""
    
    def __init__(self, host: str, username: str, password: str, port: int = 22):
        """Инициализация."""
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.ssh_client = None
        
    def connect(self) -> bool:
        """Подключиться по SSH."""
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(
                self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=10,
                look_for_keys=False,
                allow_agent=False,
            )
            _LOGGER.debug("SSH подключение установлено к %s", self.host)
            return True
        except Exception as err:
            _LOGGER.error("Ошибка SSH подключения: %s", err)
            return False
    
    def disconnect(self):
        """Отключиться."""
        if self.ssh_client:
            try:
                self.ssh_client.close()
            except:
                pass
    
    def execute_command(self, command: str) -> str:
        """Выполнить команду."""
        if not self.ssh_client:
            if not self.connect():
                raise ConnectionError("Не удалось подключиться")
        
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command, timeout=10)
            result = stdout.read().decode('utf-8', errors='ignore').strip()
            error = stderr.read().decode('utf-8', errors='ignore').strip()
            
            if error and not result:
                _LOGGER.warning("Команда '%s' вернула ошибку: %s", command, error)
            
            return result
        except Exception as err:
            _LOGGER.error("Ошибка выполнения команды '%s': %s", command, err)
            raise
    
    def get_system_info(self) -> Dict:
        """Получить всю информацию о системе."""
        data = {}
        
        # CPU Load
        try:
            output = self.execute_command("cat /proc/loadavg")
            values = output.split()
            data['cpu_load_1'] = float(values[0])
            data['cpu_load_5'] = float(values[1])
            data['cpu_load_15'] = float(values[2])
        except Exception as err:
            _LOGGER.error("Ошибка получения CPU Load: %s", err)
            data['cpu_load_1'] = 0.0
            data['cpu_load_5'] = 0.0
            data['cpu_load_15'] = 0.0
        
        # Memory
        try:
            output = self.execute_command("free -m")
            lines = output.split('\n')
            mem_line = lines[1].split()
            total = int(mem_line[1])
            used = int(mem_line[2])
            data['memory_total'] = total
            data['memory_used'] = used
            data['memory_free'] = int(mem_line[3])
            data['memory_percentage'] = round((used / total) * 100, 1) if total > 0 else 0
        except Exception as err:
            _LOGGER.error("Ошибка получения Memory: %s", err)
            data['memory_total'] = 0
            data['memory_used'] = 0
            data['memory_free'] = 0
            data['memory_percentage'] = 0
        
        # Uptime
        try:
            output = self.execute_command("cat /proc/uptime")
            uptime_seconds = int(float(output.split()[0]))
            days = uptime_seconds // 86400
            hours = (uptime_seconds % 86400) // 3600
            minutes = (uptime_seconds % 3600) // 60
            data['uptime'] = f"{days}д {hours}ч {minutes}м"
            data['uptime_seconds'] = uptime_seconds
        except Exception as err:
            _LOGGER.error("Ошибка получения Uptime: %s", err)
            data['uptime'] = "неизвестно"
            data['uptime_seconds'] = 0
        
        # Interface Traffic
        try:
            output = self.execute_command("cat /proc/net/dev")
            interfaces = {}
            lines = output.split('\n')[2:]  # Пропускаем заголовки
            
            for line in lines:
                if not line.strip():
                    continue
                parts = line.split()
                if len(parts) < 10:
                    continue
                    
                iface_name = parts[0].replace(':', '')
                interfaces[iface_name] = {
                    'rx_bytes': int(parts[1]),
                    'rx_packets': int(parts[2]),
                    'tx_bytes': int(parts[9]),
                    'tx_packets': int(parts[10]),
                }
            
            data['interfaces'] = interfaces
        except Exception as err:
            _LOGGER.error("Ошибка получения Interface Traffic: %s", err)
            data['interfaces'] = {}
        
        # Connected Devices
        try:
            output = self.execute_command("cat /proc/net/arp")
            devices = []
            lines = output.split('\n')[1:]  # Пропускаем заголовок
            
            for line in lines:
                if not line.strip():
                    continue
                parts = line.split()
                if len(parts) >= 6 and parts[3] != "00:00:00:00:00:00":
                    devices.append({
                        'ip': parts[0],
                        'mac': parts[3],
                        'interface': parts[5],
                    })
            
            data['connected_devices'] = devices
            data['connected_devices_count'] = len(devices)
        except Exception as err:
            _LOGGER.error("Ошибка получения Connected Devices: %s", err)
            data['connected_devices'] = []
            data['connected_devices_count'] = 0
        
        return data
    
    def reboot(self) -> bool:
        """Перезагрузить маршрутизатор."""
        try:
            self.execute_command("reboot")
            _LOGGER.warning("Маршрутизатор перезагружается")
            return True
        except Exception as err:
            _LOGGER.error("Ошибка перезагрузки: %s", err)
            return False