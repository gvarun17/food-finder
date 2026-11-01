"""Hybrid search: hard SQL filters first, then vector ranking among what is left."""
from typing import Any

from pgvector import Vector

from app.db import connect
from app.embeddings import embed_one

SQL = """
SELECT
    m.id, m.name AS dish, m.description, m.price_inr, m.is_veg, m.spice_level, m.course,
    r.id AS restaurant_id, r.name AS restaurant, r.area, r.address, r.phone,
    r.cuisines, r.lat, r.lng, m.updated_at,
    (m.embedding <=> %(vec)s::vector) AS distance
FROM menu_items m
JOIN restaurants r ON r.id = m.restaurant_id
WHERE m.is_available
  AND (%(include_fake)s::boolean OR NOT r.is_fake)
  AND (%(area)s::text IS NULL OR lower(r.area) = lower(%(area)s))
  AND (%(max_price)s::int IS NULL OR m.price_inr <= %(max_price)s)
  AND (%(veg_only)s::boolean IS NOT TRUE OR m.is_veg)
  AND (%(cuisine)s::text IS NULL OR EXISTS (
        SELECT 1 FROM unnest(r.cuisines) c WHERE lower(c) = lower(%(cuisine)s)))
ORDER BY m.embedding <=> %(vec)s::vector
LIMIT %(pool)s
"""


def list_areas(include_fake: bool = True) -> list[str]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT DISTINCT area FROM restaurants WHERE (%s::boolean OR NOT is_fake) ORDER BY area",
            (include_fake,),
        ).fetchall()
    return [r[0] for r in rows]


def search_dishes(
    semantic_query: str,
    area: str | None = None,
    max_price: int | None = None,
    veg_only: bool | None = None,
    cuisine: str | None = None,
    max_restaurants: int = 5,
    max_per_restaurant: int = 2,
    include_fake: bool = True,  # True while all data is dev data; set False before real users
) -> list[dict[str, Any]]:
    vec = Vector(embed_one(semantic_query or "popular dishes"))
    params = dict(
        vec=vec, area=area, max_price=max_price, veg_only=veg_only,
        cuisine=cuisine, include_fake=include_fake, pool=40,
    )
    with connect() as conn:
        cur = conn.execute(SQL, params)
        cols = [c.name for c in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]

    # Group: at most N dishes per restaurant, at most M restaurants, best match first.
    out: list[dict[str, Any]] = []
    per_rest: dict[int, int] = {}
    for row in rows:
        rid = row["restaurant_id"]
        if rid not in per_rest and len(per_rest) >= max_restaurants:
            continue
        if per_rest.get(rid, 0) >= max_per_restaurant:
            continue
        per_rest[rid] = per_rest.get(rid, 0) + 1
        row["updated_at"] = row["updated_at"].date().isoformat()
        row["distance"] = round(float(row["distance"]), 3)
        out.append(row)
    return out
