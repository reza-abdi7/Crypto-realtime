from datetime import datetime
from pydantic import BaseModel, field_serializer
from typing import Dict, Any

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
    def from_kraken_api_response(
        cls,
        pair: str,
        price: float,
        volume: float,
        timestamp: str,
    ) -> "Trade":
        """Create a Trade instance from Kraken API response"""
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return cls(
            pair=pair,
            price=price,
            volume=volume,
            timestamp=dt,
            timestamp_ms=int(dt.timestamp() * 1000)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Trade to a dictionary with serializable values"""
        return self.model_dump()