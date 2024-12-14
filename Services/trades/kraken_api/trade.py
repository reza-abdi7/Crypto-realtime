from datetime import datetime, timezone
from typing import Any, Dict

from pydantic import BaseModel, field_serializer


class Trade(BaseModel):
    """
    trade from kraken api
    """

    pair: str
    price: float
    volume: float
    timestamp: datetime
    timestamp_ms: int

    @field_serializer('timestamp')
    def serialize_datetime(self, dt: datetime) -> str:
        """Serialize datetime to ISO format string"""
        return dt.isoformat()

    @classmethod
    def from_kraken_rest_api_response(
        cls,
        pair: str,
        price: float,
        volume: float,
        timestamp_sec: float,
    ) -> 'Trade':
        """
        Returns a Trade object from the Kraken REST API response.

        E.g response:
            ['76395.00000', '0.01305597', 1731155565.4159515, 's', 'm', '', 75468573]

            price: float
            volume: float
            timestamp_sec: float
        """
        timestamp_ms = int(float(timestamp_sec) * 1000)
        dt = datetime.fromtimestamp(timestamp_ms / 1000.0, tz=timezone.utc)

        return cls(
            pair=pair,
            price=price,
            volume=volume,
            timestamp=dt,
            timestamp_ms=timestamp_ms,
        )

    @classmethod
    def from_kraken_websocket_api_response(
        cls,
        pair: str,
        price: float,
        volume: float,
        timestamp: str,
    ) -> 'Trade':
        """Create a Trade instance from Kraken API response"""
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return cls(
            pair=pair,
            price=price,
            volume=volume,
            timestamp=dt,
            timestamp_ms=int(dt.timestamp() * 1000),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert Trade to a dictionary with serializable values"""
        return self.model_dump()
