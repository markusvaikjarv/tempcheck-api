-- This enables turns the sensor_readings table into a hypertable (columnar store, partitioned by timestamps)
-- Target database is TimescaleDB
SELECT create_hypertable('sensor_readings', by_range('recorded_at'));
