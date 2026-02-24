"""CN Tower Lighting Integration."""
import asyncio
import logging
from datetime import time

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, DEFAULT_UPDATE_HOUR

PLATFORMS = [Platform.SENSOR, Platform.CALENDAR, Platform.SWITCH]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up from config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Store session
    hass.data[DOMAIN][entry.entry_id] = {
        "session": async_get_clientsession(hass),
        "update_hour": entry.data.get("update_hour", DEFAULT_UPDATE_HOUR)
    }
    
    # Auto-setup automation if enabled
    if entry.options.get("auto_update", True):
        await _create_daily_update(hass, entry)
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

async def _create_daily_update(hass: HomeAssistant, entry: ConfigEntry):
    """Create daily automation."""
    automation = {
        "alias": f"Update CN Tower Lights @ {entry.data['update_hour']}:00",
        "trigger": [{"platform": "time", "at": time(hour=entry.data["update_hour"])}],
        "action": [{"service": "homeassistant.update_entity", "entity_id": f"sensor.cn_tower_{entry.entry_id}_today"}]
    }
    # Use hass.services.async_create to register

