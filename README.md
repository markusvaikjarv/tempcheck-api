# TempCheck API

A FastAPI-based REST API for managing IoT sensor readings and analytics with MQTT integration and TimescaleDB storage.

## Features

- Real-time temperature sensor readings via MQTT
- Sensor provisioning management
- Time-series data storage in using TimescaleDB
- Authentication and authorization (OAuth 2)

## Project Structure

```
├── src/
│   ├── auth/               # Authentication handlers
│   ├── commons/           # Shared utilities
│   ├── migrations/        # SQL migrations
│   ├── provisionings/     # Sensor provisioning
│   └── sensor_readings/   # Sensor readings
├── main.py               # Application entry
├── mqtt_listener.py      # MQTT client implementation
├── generate_fake_data.py # Test data generator
└── requirements.txt      # Python dependencies
```