#!/usr/bin/env python3
"""Load compiled ISPA CSVs into data/ispa_indonesia.db (SQLite).

The dataset is COMPILED from official published figures (see data/SOURCES.md).
This script only loads the CSVs and verifies row counts - it invents nothing.
"""
import csv
import os
import sqlite3

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPILED = os.path.join(HERE, "data", "compiled")
DB = os.path.join(HERE, "data", "ispa_indonesia.db")

TABLES = {
    "skdr_provinsi": "skdr_provinsi_2026.csv",
    "karhutla_series": "karhutla_series.csv",
    "karhutla_provinsi": "karhutla_provinsi.csv",
    "ispu_wilayah": "ispu_wilayah.csv",
    "jakarta_bulanan": "jakarta_bulanan.csv",
    "mingguan_nasional": "mingguan_nasional.csv",
}


def main():
    if os.path.exists(DB):
        os.remove(DB)
    con = sqlite3.connect(DB)
    cur = con.cursor()
    for table, fname in TABLES.items():
        path = os.path.join(COMPILED, fname)
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        cols = list(rows[0].keys())
        cur.execute(
            f"CREATE TABLE {table} ({', '.join(f'\"{c}\" TEXT' for c in cols)})"
        )
        cur.executemany(
            f"INSERT INTO {table} VALUES ({', '.join('?' * len(cols))})",
            [[r[c] for c in cols] for r in rows],
        )
        print(f"{table}: {len(rows)} rows")
    con.commit()
    # Verification: totals that must match the published figures
    total_top10 = cur.execute(
        "SELECT SUM(CAST(kasus_skdr_2026 AS INTEGER)) FROM skdr_provinsi"
    ).fetchone()[0]
    print(f"Top-10 SKDR sum: {total_top10:,} (must be 10,530,385)")
    assert total_top10 == 10530385, "Top-10 sum mismatch!"
    karhutla_total = cur.execute(
        "SELECT kasus_kumulatif FROM karhutla_series WHERE tanggal='2026-10-13'"
    ).fetchone()[0]
    print(f"Karhutla total 13 Okt: {karhutla_total} (must be 283270)")
    assert karhutla_total == "283270", "Karhutla total mismatch!"
    con.close()
    print(f"Database written: {DB}")


if __name__ == "__main__":
    main()
