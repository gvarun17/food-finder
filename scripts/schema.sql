CREATE EXTENSION IF NOT EXISTS vector;

DROP TABLE IF EXISTS menu_items;
DROP TABLE IF EXISTS restaurants;

CREATE TABLE restaurants (
    id            SERIAL PRIMARY KEY,
    name          TEXT NOT NULL,
    area          TEXT NOT NULL,
    address       TEXT,
    lat           DOUBLE PRECISION,
    lng           DOUBLE PRECISION,
    phone         TEXT,
    cuisines      TEXT[] NOT NULL DEFAULT '{}',
    price_band    SMALLINT,            -- 1 cheap .. 4 expensive
    hours         JSONB,               -- not used for filtering yet
    is_fake       BOOLEAN NOT NULL DEFAULT FALSE,  -- dev data; never ship to users
    source        TEXT NOT NULL DEFAULT 'manual',
    verified_at   TIMESTAMPTZ,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE menu_items (
    id            SERIAL PRIMARY KEY,
    restaurant_id INTEGER NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
    name          TEXT NOT NULL,
    description   TEXT,
    price_inr     INTEGER NOT NULL CHECK (price_inr > 0),
    is_veg        BOOLEAN NOT NULL,
    spice_level   SMALLINT,            -- 0 none .. 3 very spicy
    course        TEXT,                -- starter, main, dessert, drink, ...
    is_available  BOOLEAN NOT NULL DEFAULT TRUE,
    tags          TEXT[] NOT NULL DEFAULT '{}',
    embedding     vector(384),         -- must match EMBEDDING_DIM
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_restaurants_area ON restaurants (lower(area));
CREATE INDEX idx_items_restaurant ON menu_items (restaurant_id);
CREATE INDEX idx_items_price ON menu_items (price_inr);
CREATE INDEX idx_items_embedding ON menu_items USING hnsw (embedding vector_cosine_ops);
