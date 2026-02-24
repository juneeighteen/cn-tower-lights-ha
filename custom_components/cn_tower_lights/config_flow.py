"""Config flow."""
import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector
from .const import DOMAIN
from .const import CONF_UPDATE_HOUR, DEFAULT_UPDATE_HOUR

STEP_USER = "user"
STEP_REAUTH = "reauth"

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow handler."""

    @staticmethod
    @config_entries.HANDLERS.register(DOMAIN)
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle user setup."""
        errors = {}
        
        if user_input:
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data={
                    CONF_UPDATE_HOUR: user_input[CONF_UPDATE_HOUR],
                },
                options={"auto_update": True}
            )
        
        schema = vol.Schema({
            vol.Required(CONF_NAME, default="CN Tower Lights"): selector.TextSelector(),
            vol.Required(CONF_UPDATE_HOUR, default=DEFAULT_UPDATE_HOUR): selector.NumberSelector(
                { "min": 0, "max": 23, "mode": "slider" }
            )
        })
        
        return self.async_show_form(
            step_id=STEP_USER,
            data_schema=schema,
            errors=errors
        )

class OptionsFlowHandler(config_entries.OptionsFlow):
    """Options flow."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage options."""
        if user_input:
            return self.async_create_entry(title="", data=user_input)
        
        schema = vol.Schema({
            "auto_update": selector.BooleanSelector(config_entry.options.get("auto_update", True))
        })
        return self.async_show_form(
            step_id="init",
            data_schema=schema
        )

