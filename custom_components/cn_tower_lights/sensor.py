"""CN Tower Lights sensors."""
import re
import logging
from datetime import datetime

import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util.dt import utcnow

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, 
    entry: ConfigEntry, 
    async_add_entities
):
    """Set up sensor entry."""
    session = hass.data[DOMAIN][entry.entry_id]["session"]
    coordinator = CNTowerDataCoordinator(hass, entry.title, session)
    await coordinator.async_config_entry_first_refresh()
    
    async_add_entities([
        CNTowerTodaySensor(coordinator, entry.entry_id, entry.title)
    ])

class CNTowerDataCoordinator(DataUpdateCoordinator):
    """Data coordinator for CN Tower lights."""

    def __init__(self, hass, name, session):
        super().__init__(
            hass,
            _LOGGER,
            name=f"CN Tower {name}",
            update_interval=86400,  # 24 hours
        )
        self.session = session

    async def _async_update_data(self):
        """Fetch data from CN Tower."""
        headers

