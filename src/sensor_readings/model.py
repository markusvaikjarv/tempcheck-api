from datetime import datetime
from typing import List
import asyncpg
from src.sensor_readings.schemas import GroupBy, GroupedSensorReadings, HistoricSensorReadings, SensorReading, LatestSensorReadings, AverageSensorReading, AverageSensorReadings
from src.commons.postgres import database
import json

async def get_historic_sensor_readings(user_id: str, provisioning_ids: List[str], start_datetime: datetime, end_datetime: datetime) -> HistoricSensorReadings:
    query = """
        SELECT sensor_readings.id, provisioning_id, recorded_at, temperature, humidity 
        FROM sensor_readings JOIN provisionings ON sensor_readings.provisioning_id = provisionings.id
        WHERE provisioning_id = ANY($1::uuid[]) 
        AND recorded_at BETWEEN $2 AND $3
        AND provisionings.user_id = $4
        ORDER BY provisioning_id, recorded_at DESC
    """
    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, provisioning_ids, start_datetime, end_datetime, user_id)
        grouped_readings = {}
        for row in rows:
            provisioning_id = str(row['provisioning_id'])
            if provisioning_id not in grouped_readings:
                grouped_readings[provisioning_id] = []
            grouped_readings[provisioning_id].append(SensorReading(recorded_at=row['recorded_at'], temperature=row['temperature'], humidity=row['humidity']))

        return HistoricSensorReadings(grouped_readings)

async def get_historic_sensor_readings_grouped(user_id: str, provisioning_ids: List[str], start_datetime: datetime, end_datetime: datetime, by: GroupBy) -> GroupedSensorReadings:
    time_bucket_expr = {
        'minute': "date_trunc('minute', recorded_at)",
        'hour':   "date_trunc('hour', recorded_at)",
        'day':    "date_trunc('day', recorded_at)",
        'month':  "date_trunc('month', recorded_at)"
    }[by]

    query = f"""
    SELECT
        provisioning_id,
        jsonb_object_agg(
            to_char(bucket_dt, 'YYYY-MM-DD HH24:MI:SS'),
            jsonb_build_object(
                'temp', jsonb_build_object(
                    'low',     temp_low,
                    'average', temp_avg,
                    'high',    temp_high
                ),
                'humidity', jsonb_build_object(
                    'low',     humidity_low,
                    'average', humidity_avg,
                    'high',    humidity_high
                )
            )
            ORDER BY bucket_dt
        ) AS data
    FROM (
        SELECT
            provisioning_id,
            {time_bucket_expr} AS bucket_dt,
            MIN(temperature)  AS temp_low,
            ROUND(AVG(temperature)::numeric, 2) AS temp_avg,
            MAX(temperature)  AS temp_high,
            MIN(humidity)     AS humidity_low,
            ROUND(AVG(humidity)::numeric, 2) AS humidity_avg,
            MAX(humidity)     AS humidity_high
        FROM sensor_readings
        JOIN provisionings ON sensor_readings.provisioning_id = provisionings.id
        WHERE provisioning_id = ANY($1::uuid[])
        AND recorded_at >= $2
        AND recorded_at <= $3
        AND provisionings.user_id = $4
        GROUP BY provisioning_id, {time_bucket_expr}
    ) agg
    GROUP BY provisioning_id
    """
    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, provisioning_ids, start_datetime, end_datetime, user_id)
        grouped_readings = {}
        for row in rows:
            provisioning_id = str(row['provisioning_id'])
            grouped_readings[provisioning_id] = json.loads(row['data'])
        return GroupedSensorReadings(grouped_readings)


async def get_latest_sensor_readings(user_id, provisioning_ids: List[str]) -> LatestSensorReadings:
    query = """
        SELECT DISTINCT ON (provisioning_id) provisioning_id, recorded_at, temperature, humidity
        FROM sensor_readings JOIN provisionings ON sensor_readings.provisioning_id = provisionings.id
        WHERE provisioning_id = ANY($1::uuid[])
        AND provisionings.user_id = $2
        ORDER BY provisioning_id, recorded_at DESC
    """
    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, provisioning_ids, user_id)
        latest_readings = {}
        for row in rows:
            provisioning_id = str(row['provisioning_id'])
            latest_readings[provisioning_id] = SensorReading(
                recorded_at=row['recorded_at'],
                temperature=row['temperature'],
                humidity=row['humidity']
            )

        return LatestSensorReadings(latest_readings)

async def get_average_sensor_readings(user_id: str, provisioning_ids: List[str], start_datetime: datetime, end_datetime: datetime) -> AverageSensorReadings:
    query = """
        SELECT provisioning_id, AVG(temperature) as avg_temperature, AVG(humidity) as avg_humidity
        FROM sensor_readings JOIN provisionings ON sensor_readings.provisioning_id = provisionings.id
        WHERE provisioning_id = ANY($1::uuid[])
        AND recorded_at BETWEEN $2 AND $3
        AND provisionings.user_id = $4
        GROUP BY provisioning_id
    """
    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, provisioning_ids, start_datetime, end_datetime, user_id)
        average_readings = {}
        for row in rows:
            provisioning_id = str(row['provisioning_id'])
            average_readings[provisioning_id] = AverageSensorReading(temperature=row['avg_temperature'], humidity=row['avg_humidity'])

        return AverageSensorReadings(average_readings)

async def create_sensor_reading(provisioning_id: str, temperature: float, humidity: float) -> bool:
    query = "INSERT INTO sensor_readings (provisioning_id, temperature, humidity) VALUES ($1, $2, $3)"
    async with database.pool.acquire() as connection:
        try:
            await connection.execute(query, provisioning_id, temperature, humidity)
        except asyncpg.exceptions.ForeignKeyViolationError:
            # The provisioning_id does not exist - probably deleted. We don't have consent to store the data.
            return False
        return True
    
