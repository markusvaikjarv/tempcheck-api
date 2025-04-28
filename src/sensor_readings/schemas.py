from pydantic import BaseModel, RootModel
from datetime import datetime
from enum import Enum
from typing import Dict
from uuid import UUID

ProvisioningId = UUID

class GroupBy(str, Enum):
    minute = "minute"
    hour = "hour"
    day = "day"
    month = "month"

class SensorReading(BaseModel):
    recorded_at: datetime
    temperature: float
    humidity: float

class AverageSensorReading(BaseModel):
    temperature: float
    humidity: float

HistoricSensorReadings = RootModel[dict[ProvisioningId, list[SensorReading]]]
LatestSensorReadings = RootModel[dict[ProvisioningId, SensorReading]]
AverageSensorReadings = RootModel[dict[ProvisioningId, AverageSensorReading]]

class GroupStats(BaseModel):
    low: float
    average: float
    high: float

class GroupedReading(BaseModel):
    temp: GroupStats
    humidity: GroupStats

GroupedSensorReadings = RootModel[Dict[ProvisioningId, Dict[datetime, GroupedReading]]]