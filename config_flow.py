"""Config flow for D-Link Router."""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import callback

from .api import DLinkRouterAPI
from .const import DOMAIN, DEFAULT_HOST, DEFAULT_USERNAME, DEFAULT_PORT, CONF_SSH_PORT

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
    vol.Required(CONF_USERNAME, default=DEFAULT_USERNAME): str,
    vol.Required(CONF_PASSWORD): str,
    vol.Optional(CONF_SSH_PORT, default=DEFAULT_PORT): int,
})


class DLinkRouterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow для D-Link Router."""
    
    VERSION = 1
    
    async def async_step_user(self, user_input=None):
        """Шаг 1: Ввод данных пользователем."""
        
        errors = {}
        
        if user_input is not None:
            # Тестируем подключение
            host = user_input[CONF_HOST]
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]
            port = user_input.get(CONF_SSH_PORT, DEFAULT_PORT)
            
            try:
                # Проверяем подключение
                api = DLinkRouterAPI(host, username, password, port)
                connected = await self.hass.async_add_executor_job(api.connect)
                
                if not connected:
                    errors["base"] = "cannot_connect"
                else:
                    # Отключаемся
                    await self.hass.async_add_executor_job(api.disconnect)
                    
                    # Создаём entry
                    return self.async_create_entry(
                        title=f"D-Link Router ({host})",
                        data=user_input,
                    )
                    
            except Exception:
                errors["base"] = "unknown"
        
        # Показываем форму
        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )