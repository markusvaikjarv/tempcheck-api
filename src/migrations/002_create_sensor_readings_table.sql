CREATE TABLE sensor_readings (
    id UUID DEFAULT uuid_generate_v4(),
    provisioning_id UUID NOT NULL,
    temperature FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    recorded_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (provisioning_id) REFERENCES provisionings(id) ON DELETE CASCADE
);