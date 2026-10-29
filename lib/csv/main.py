from __future__ import annotations

import csv
from pathlib import Path


CSV_DIR = Path(__file__).parent
OUTPUT_FILE = CSV_DIR.parent / "libri.csv"


def combine_csv_files() -> None:
    csv_files = sorted(
        file
        for file in CSV_DIR.glob("*.csv")
        if file.resolve() != OUTPUT_FILE.resolve()
    )

    if not csv_files:
        raise FileNotFoundError(f"Nessun file CSV trovato in {CSV_DIR}")

    rows: list[dict[str, str]] = []
    fieldnames: list[str] = []

    for csv_file in csv_files:
        with csv_file.open("r", encoding="utf-8-sig", newline="") as file:
            sample = file.read(4096)
            file.seek(0)

            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
            reader = csv.DictReader(file, dialect=dialect)
            if not reader.fieldnames:
                continue

            for field in reader.fieldnames:
                if field and field not in fieldnames:
                    fieldnames.append(field)

            rows.extend(
                {
                    key: (value or "").strip()
                    for key, value in row.items()
                    if key
                }
                for row in reader
            )

    if not fieldnames:
        raise ValueError("I file CSV non contengono intestazioni valide")

    with OUTPUT_FILE.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            delimiter=";",
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Creato {OUTPUT_FILE} con {len(rows)} righe da {len(csv_files)} file.")


if __name__ == "__main__":
    combine_csv_files()