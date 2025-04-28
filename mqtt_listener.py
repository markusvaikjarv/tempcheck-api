from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

import asyncio
from asyncio_mqtt import Client
from src.commons.postgres import database
from src.sensor_readings.model import create_sensor_reading
import ssl
import json

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_PORT = 8883
MQTT_TOPIC = "sensor_readings/#"

cached_queue = asyncio.Queue()

async def consume_messages():
    if not isinstance(MQTT_BROKER, str):
        raise ValueError("MQTT_BROKER must be a string")

    ssl_context = ssl.create_default_context()
    async with Client(hostname=MQTT_BROKER, port=MQTT_PORT, username=MQTT_USERNAME, password=MQTT_PASSWORD, tls_context=ssl_context) as client:
        await client.subscribe(MQTT_TOPIC)
        async with client.messages() as messages:
            async for message in messages:
                if isinstance(message.payload, (bytes, bytearray, str)):
                    data = json.loads(message.payload)
                    data['provisioning_id'] = str(message.topic).split('/')[-1]
                    await cached_queue.put(data)

async def flush_cache_to_db():
    await database.connect()
    while True:
        await asyncio.sleep(10)  # Flush the cache every 10 seconds

        to_save = []
        while not cached_queue.empty():
            msg = await cached_queue.get()
            to_save.append(msg)

        for reading in to_save:
            print(reading['provisioning_id'])
            await create_sensor_reading(
                provisioning_id=reading['provisioning_id'],
                temperature=reading['temperature'],
                humidity=reading['humidity']
            )

async def main():
    consumer_task = asyncio.create_task(consume_messages())
    saver_task = asyncio.create_task(flush_cache_to_db())

    await asyncio.gather(consumer_task, saver_task)

if __name__ == "__main__":
    asyncio.run(main())
