PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS dim_station (
    station_key TEXT PRIMARY KEY,
    station_name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS fact_rental_hour (
    station_key TEXT NOT NULL REFERENCES dim_station(station_key),
    hour TEXT NOT NULL,
    rental_count INTEGER NOT NULL CHECK (rental_count >= 0),
    temperature REAL,
    PRIMARY KEY (station_key, hour)
);
CREATE VIEW IF NOT EXISTS mart_rental_day AS
SELECT station_key, substr(hour, 1, 10) AS day,
       COUNT(*) AS observed_hours,
       SUM(rental_count) AS rental_count,
       AVG(temperature) AS mean_temperature
FROM fact_rental_hour
GROUP BY station_key, substr(hour, 1, 10);
