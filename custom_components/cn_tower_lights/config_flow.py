"""Config flow."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import DOMAIN, CONF_NAME, DEFAULT_NAME  # <-- FIX #1: Import CONF_NAME!

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """ConfigFlow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle user step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_only")

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data={CONF_NAME: user_input[CONF_NAME]}
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default=DEFAULT_NAME): selector.TextSelector()
            })
        )

