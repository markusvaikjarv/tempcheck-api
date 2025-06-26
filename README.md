# TempCheck API

A FastAPI-based REST API for managing IoT sensor readings and analytics with MQTT integration and TimescaleDB storage.

## Features

- Real-time temperature sensor readings via MQTT
- Sensor provisioning management
- Time-series data storage in using TimescaleDB
- Authentication and authorization (OAuth 2)

## Structure
```mermaid
graph TD
    A(((Temperature Sensor))) -- "MQTT" --> B{{Broker}};
    B -- "MQTT" --> C[TempCheck API];
    C --> D[(TimescaleDB OLAP Database)];
    E[API Client] --> C;
    C -- "OAuth2" --> G[Keycloak Auth Server];
    E -- "OAuth2" --> G;

    style A fill:#ffa500,stroke:#333,stroke-width:2px;
    style E fill:#f9f,stroke:#333,stroke-width:2px;
    style G fill:#9f9,stroke:#333,stroke-width:2px;
```
