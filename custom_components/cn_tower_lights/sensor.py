"""Sensors."""
import re
import logging
from datetime import datetime

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SENSOR_TODAY

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Setup sensors."""
    session = hass.data[DOMAIN][entry.entry_id]["session"]
    
    coordinator = CNTowerDataCoordinator(hass, session, entry.entry_id)
    await coordinator.async_config_entry_first_refresh()
    
    async_add_entities([
        CNTowerTodaySensor(coordinator, entry),
        CNTowerEventsSensor(coordinator, entry)
    ])

class CNTowerDataCoordinator(DataUpdateCoordinator):
    """Data coordinator."""

    def __init__(self, hass, session, entry_id):
        super().__init__(
            hass,
            _LOGGER,
            name="CN Tower Lights",
            update_interval=86400  # 1 day
        )
        self._session = session
        self._entry_id = entry_id

    async def _async_update_data(self):
        """Fetch data."""
        headers = {
            "User-Agent": "Mozilla/5.0 (HA CN Tower Integration)"
        }
        try:
            async with self._session.get(
                "https://www.cntower.ca/lighting-calendar",
                headers=headers,
                timeout=30
            ) as resp:
                html = await resp.text()
                
            # Regex parse (adjust after inspection)
            events = {}
            date_pattern = r'(\w{3}\s+\d{1,2},?\s+\d{4})[^<]*?(light|red|blue|green|rainbow|white|pride)[^<]*?(?:#([0-9a-fA-F]{6}))?'
            for match in re.finditer(date_pattern, html, re.IGNORECASE | re.DOTALL):
                date_str, theme, color = match.groups()
                try:
                    date_obj = datetime.strptime(date_str.strip(), '%b %d, %Y')
                    date_key = date_obj.strftime('%Y-%m-%d')
                    events[date_key] = {
                        "title": f"{theme.title()} Lighting",
                        "color": f"#{color}" if color else "#FFFFFF"
                    }
                except ValueError:
                    continue
            
            today = datetime.now().strftime('%Y-%m-%d')
            return {
                "today": events.get(today, {"title": "Default White", "color": "#FFFFFF"}),
                "events": list(events.items())[:30]  # Next 30 days
            }
        except Exception as err:
            raise UpdateFailed(f"Error fetching CN Tower data: {err}")

class CNTowerTodaySensor(SensorEntity):
    """Today sensor."""

    def __init__(self, coordinator, entry):
        self.coordinator = coordinator
        self._entry_id = entry.entry_id
        self.entity_id = f"sensor.cn_tower_{entry.entry_id}_today"
        self._attr_name = "CN Tower Today"
        self._attr_unique_id = f"cn_tower_today_{entry.entry_id}"
        self._attr_icon = "mdi:lightbulb-outline"

    @property
    def native_value(self):
        return self.coordinator.data["today"]["title"]

    @property
    def extra_state_attributes(self):
        return {
            "color": self.coordinator.data["today"]["color"],
            "events": self.coordinator.data["events"]
        }

    @property
    def available(self):
        return self.coordinator.last_update_success

    async def async_update(self):
        await self.coordinator.async_request_refresh()

class CNTowerEventsSensor(SensorEntity):
    """Events list."""
    # Similar, state = len(events), attrs = events dict

