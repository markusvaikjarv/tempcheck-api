from dotenv import load_dotenv
load_dotenv()

from src.commons.postgres import database
import asyncpg
import asyncio
import random
from datetime import datetime, timedelta

async def main():
    await database.connect()

    provisioning_id = '570aba81-21af-4114-8e55-a977a82de2c5'

    start_date = datetime(2025, 2, 10, 0, 0)
    end_date   = datetime(2025, 2, 20, 23, 59)

    time_delta = timedelta(minutes=30)
    current = start_date

    count = 0
    async with database.pool.acquire() as connection:
        query = "INSERT INTO sensor_readings (provisioning_id, temperature, humidity, created_at, recorded_at) VALUES ($1, $2, $3, $4, $5)"

        while current <= end_date:
            print(f"Inserting {count}th record")
            temperature = random.uniform(22.5, 25.5)
            humidity = random.uniform(33, 38)

            res = await connection.execute(query, provisioning_id, temperature, humidity, current, current)
            print(query, provisioning_id, temperature, humidity, current, current)

            current += time_delta
            count += 1

if __name__ == '__main__':
    asyncio.run(main())
