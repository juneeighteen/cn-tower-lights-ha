"""Calendar platform."""
from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.core import callback

class CNTowerCalendar(CalendarEntity):
    """Lighting calendar."""

    def __init__(self, coordinator, entry):
        self.coordinator = coordinator
        self._entry_id = entry.entry_id
        self._attr_name = "CN Tower Lighting Schedule"
        self._attr_unique_id = f"cn_tower_calendar_{entry.entry_id}"

    @property
    def event(self) -> CalendarEvent | None:
        """Return next event."""
        events = self.coordinator.data["events"]
        if events:
            date_str, data = events[0]
            return CalendarEvent(
                start=date_str,
                end=date_str,
                summary=data["title"],
                color=data["color"]
            )
        return None

    async def async_get_events(self, hass, start_date, end_date):
        """Get events."""
        # Return all matching events
        pass  # Implement list

