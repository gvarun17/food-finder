"""Load fake dev data and embeddings: python -m scripts.seed"""
from pgvector import Vector

from app.db import connect
from app.embeddings import embed
from scripts.seed_data import RESTAURANTS


def item_text(dish: str, desc: str, cuisines: list[str], course: str, veg: bool) -> str:
    return f"{dish}. {desc}. {', '.join(cuisines)} {course}. {'vegetarian' if veg else 'non-vegetarian'}"


def main() -> None:
    rows = []  # (restaurant index, dish tuple, text)
    for ri, r in enumerate(RESTAURANTS):
        for d in r["dishes"]:
            rows.append((ri, d, item_text(d[0], d[1], r["cuisines"], d[5], d[3])))

    print(f"Embedding {len(rows)} dishes (first run downloads the model)...")
    vectors = embed([t for _, _, t in rows])

    with connect() as conn:
        conn.execute("TRUNCATE menu_items, restaurants RESTART IDENTITY CASCADE")
        rest_ids = []
        for r in RESTAURANTS:
            rid = conn.execute(
                """INSERT INTO restaurants (name, area, cuisines, price_band, is_fake, source, verified_at)
                   VALUES (%s, %s, %s, %s, TRUE, 'seed', now()) RETURNING id""",
                (r["name"], r["area"], r["cuisines"], r["price_band"]),
            ).fetchone()[0]
            rest_ids.append(rid)
        for (ri, d, _), vec in zip(rows, vectors):
            name, desc, price, veg, spice, course = d
            conn.execute(
                """INSERT INTO menu_items
                   (restaurant_id, name, description, price_inr, is_veg, spice_level, course, embedding)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (rest_ids[ri], name, desc, price, veg, spice, course, Vector(vec)),
            )
        conn.commit()
    print(f"Loaded {len(RESTAURANTS)} restaurants and {len(rows)} dishes (all marked is_fake).")


if __name__ == "__main__":
    main()
