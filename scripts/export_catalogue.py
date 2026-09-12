"""Export version-friendly Almanac catalogue data without private chat history."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE = ROOT / "localdata" / "almanac.db"
DEFAULT_OUTPUT = ROOT / "snapshots" / "almanac-catalogue.json"

CATALOGUE_TABLES = (
    "rotation_groups",
    "pests",
    "diseases",
    "function_tags",
    "uses",
    "plant_references",
    "planting_months",
    "plant_images",
    "plant_pests",
    "plant_diseases",
    "plant_function_tags",
    "plant_uses",
    "plant_companions",
)


def rows_for(connection: sqlite3.Connection, table: str) -> list[dict]:
    columns = [row["name"] for row in connection.execute(f'PRAGMA table_info("{table}")')]
    if not columns:
        raise RuntimeError(f"Expected catalogue table is missing: {table}")
    order = ", ".join(f'"{column}"' for column in columns)
    return [dict(row) for row in connection.execute(f'SELECT * FROM "{table}" ORDER BY {order}')]


def export(database: Path, output: Path) -> None:
    if not database.is_file():
        raise FileNotFoundError(f"Database not found: {database}")
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row
        schema_row = connection.execute("SELECT version_num FROM alembic_version").fetchone()
        if schema_row is None:
            raise RuntimeError("Database has no Alembic schema version.")
        tables = {table: rows_for(connection, table) for table in CATALOGUE_TABLES}
    payload = {
        "snapshot_format": 1,
        "exported_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "schema_version": schema_row["version_num"],
        "tables": tables,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    temporary.replace(output)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    arguments = parser.parse_args()
    export(arguments.database.resolve(), arguments.output.resolve())
    print(f"Exported catalogue to {arguments.output.resolve()}")


if __name__ == "__main__":
    main()
