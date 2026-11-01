"""Create the schema: python -m scripts.init_db   (WARNING: drops existing tables)"""
from pathlib import Path

from app.db import connect


def main() -> None:
    sql = (Path(__file__).parent / "schema.sql").read_text()
    with connect() as conn:
        conn.execute(sql)
        conn.commit()
    print("Schema created.")


if __name__ == "__main__":
    main()
