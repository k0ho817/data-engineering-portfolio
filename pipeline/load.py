"""Load the existing hourly bike dataset into a reproducible SQLite mart."""
import argparse
import csv
from datetime import datetime, timedelta
import hashlib
import json
import math
from pathlib import Path
import sqlite3

STATION = "yeouinaru_exit_1"
SCHEMA = Path(__file__).with_name("schema.sql")


def connect(path):
    connection = sqlite3.connect(path)
    connection.executescript(SCHEMA.read_text())
    return connection


def load(connection, source):
    records, seen = [], set()
    with Path(source).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not {"dateTime", "rental_count", "temperature"}.issubset(reader.fieldnames or []):
            raise ValueError("Missing required CSV columns")
        for row in reader:
            hour = datetime.strptime(row["dateTime"], "%Y-%m-%d %H:%M:%S")
            if hour.minute or hour.second or hour.year != 2023:
                raise ValueError("Expected an hourly timestamp in 2023")
            count = float(row["rental_count"])
            if not math.isfinite(count) or count < 0 or not count.is_integer():
                raise ValueError("Rental count must be a nonnegative integer")
            temperature = float(row["temperature"]) if row["temperature"] else None
            if temperature is not None and not math.isfinite(temperature):
                raise ValueError("Non-finite temperature")
            key = hour.isoformat(sep=" ")
            if key in seen:
                raise ValueError("Duplicate source hour: " + key)
            seen.add(key)
            records.append((STATION, key, int(count), temperature))
    if not records:
        raise ValueError("Empty input")
    # Validate the entire input before changing any existing rows.
    with connection:
        connection.execute("INSERT OR IGNORE INTO dim_station VALUES (?, ?)",
                           (STATION, "Yeouinaru Station Exit 1"))
        connection.executemany("""
            INSERT INTO fact_rental_hour VALUES (?, ?, ?, ?)
            ON CONFLICT(station_key, hour) DO UPDATE SET
              rental_count=excluded.rental_count, temperature=excluded.temperature
        """, records)
    return len(records)


def snapshot(connection):
    rows = connection.execute("SELECT * FROM fact_rental_hour ORDER BY station_key, hour").fetchall()
    return hashlib.sha256(json.dumps(rows).encode()).hexdigest()


def quality(connection):
    count, total = connection.execute("SELECT COUNT(*), SUM(rental_count) FROM fact_rental_hour").fetchone()
    observed = {r[0] for r in connection.execute("SELECT hour FROM fact_rental_hour WHERE station_key=?", (STATION,))}
    beginning = datetime(2023, 1, 1)
    expected = {(beginning + timedelta(hours=i)).isoformat(sep=" ") for i in range(8760)}
    missing = sorted(expected - observed)
    return dict(source="2023 hourly dataset; existing notebook export, not raw rentals",
                station=STATION, timezone="Asia/Seoul (source local timestamps)",
                expected_hours=8760, observed_hours=count, rental_count=total,
                missing_hours=missing, completeness_percent=round(count / 8760 * 100, 4),
                status="warning" if missing else "pass")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--database", default=":memory:")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with connect(args.database) as connection:
        load(connection, args.source)
        before = snapshot(connection)
        load(connection, args.source)
        assert before == snapshot(connection), "Rerun changed the stored dataset"
        report = quality(connection)
        report["identical_rerun"] = "pass"
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / "bike-quality.json").write_text(json.dumps(report, indent=2) + "\n")
        with (args.output / "bike-daily.csv").open("w", newline="") as target:
            cursor = connection.execute("SELECT * FROM mart_rental_day ORDER BY day")
            writer = csv.writer(target)
            writer.writerow([column[0] for column in cursor.description])
            writer.writerows(cursor)
        print(json.dumps(report))


if __name__ == "__main__":
    main()
