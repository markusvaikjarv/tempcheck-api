from fastapi import APIRouter, Depends, Query
from typing import Annotated, List
from src.sensor_readings.schemas import GroupBy
from src.sensor_readings import model
from datetime import datetime, timedelta
from src.auth.authorizers import get_user_id

router = APIRouter(prefix="/sensor-readings")

@router.get("/historic")
async def get_historic_sensor_readings(
    user_id: Annotated[str, Depends(get_user_id)],
    provisioning_ids: List[str] = Query(...),
    start_datetime: datetime = Query(datetime.fromtimestamp(0)),
    end_datetime: datetime = Query(default_factory=lambda: datetime.now() + timedelta(hours=48))
):
    return await model.get_historic_sensor_readings(user_id, provisioning_ids, start_datetime, end_datetime)

@router.get("/historic/grouped")
async def get_historic_sensor_readings_grouped(
    user_id: Annotated[str, Depends(get_user_id)],
    provisioning_ids: List[str] = Query(...),
    start_datetime: datetime = Query(datetime.fromtimestamp(0)),
    end_datetime: datetime = Query(default_factory=lambda: datetime.now() + timedelta(hours=48)),
    by: GroupBy = Query(GroupBy.hour)
):
    return await model.get_historic_sensor_readings_grouped(user_id, provisioning_ids, start_datetime, end_datetime, by)

@router.get("/latest")
async def get_latest_sensor_readings(user_id: Annotated[str, Depends(get_user_id)], provisioning_ids: List[str] = Query(...)):
    return await model.get_latest_sensor_readings(user_id, provisioning_ids)

@router.get("/average")
async def get_average_readings(
    user_id: Annotated[str, Depends(get_user_id)],
    provisioning_ids: List[str] = Query(...),
    start_datetime: datetime = Query(datetime.fromtimestamp(0)),
    end_datetime: datetime = Query(default_factory=lambda: datetime.now() + timedelta(hours=48))
):
    return await model.get_average_sensor_readings(user_id, provisioning_ids, start_datetime, end_datetime)