import csv
from pathlib import Path
import tempfile
import unittest
from load import connect, load, snapshot


class LoadTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.source = Path(self.directory.name) / "source.csv"
        self.db = connect(":memory:")
        self.addCleanup(self.directory.cleanup)
        self.addCleanup(self.db.close)

    def write(self, rows):
        with self.source.open("w", newline="") as target:
            writer = csv.writer(target)
            writer.writerow(["dateTime", "rental_count", "temperature"])
            writer.writerows(rows)

    def test_rerun_and_corrected_backfill(self):
        self.write([("2023-01-01 00:00:00", 2, 1), ("2023-01-01 01:00:00", 4, 2)])
        load(self.db, self.source)
        before = snapshot(self.db)
        load(self.db, self.source)
        self.assertEqual(before, snapshot(self.db))
        self.write([("2023-01-01 00:00:00", 3, 1)])
        load(self.db, self.source)
        self.assertEqual(self.db.execute("SELECT COUNT(*), SUM(rental_count) FROM fact_rental_hour").fetchone(), (2, 7))
        self.assertEqual(self.db.execute("SELECT observed_hours, rental_count FROM mart_rental_day").fetchone(), (2, 7))

    def test_invalid_batch_preserves_existing_data(self):
        self.write([("2023-01-01 00:00:00", 2, 1)])
        load(self.db, self.source)
        before = snapshot(self.db)
        for invalid in [-1, "NaN", 1.5]:
            self.write([("2023-01-01 00:00:00", 9, 1), ("2023-01-01 01:00:00", invalid, 2)])
            with self.assertRaises(ValueError):
                load(self.db, self.source)
            self.assertEqual(before, snapshot(self.db))

    def test_duplicate_hour_rejected(self):
        self.write([("2023-01-01 00:00:00", 2, 1)] * 2)
        with self.assertRaises(ValueError):
            load(self.db, self.source)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM fact_rental_hour").fetchone()[0], 0)


if __name__ == "__main__":
    unittest.main()
