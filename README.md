# Hyderabad Food Finder — dev setup (v0.1)

Chat with Claude to find dishes across Hyderabad restaurants. Search is hybrid: SQL filters
(area, budget, veg, cuisine) then vector ranking in Postgres + pgvector. Claude only reports what the
search tool returns. Owner updates come later.

> All data in `scripts/seed_data.py` is **invented** and marked `is_fake`. Do not show it to real users.

## Run it on your Mac

Prerequisites: [uv](https://docs.astral.sh/uv/), Docker Desktop or OrbStack.

```bash
brew install uv                     # skip if installed
brew install --cask orbstack        # or Docker Desktop; start it once

cp .env.example .env                # then put your real ANTHROPIC_API_KEY in .env
docker compose up -d                # Postgres + pgvector on :5432
uv sync                             # installs deps (torch is large; first run takes a few minutes)

uv run python -m scripts.init_db    # create tables  (drops existing ones!)
uv run python -m scripts.seed       # fake data + embeddings (downloads the embedding model once)
uv run python -m scripts.run_eval   # deterministic search checks, no API cost
uv run python chat.py -v            # terminal chat; -v prints tool calls
```

Try: `veg starters under 250 in Gachibowli`, `something spicy near Madhapur`, `haleem in Banjara Hills`,
`I want a sweet dessert`, then something impossible like `biryani under 10 rupees`.

API (optional): `uv run uvicorn app.main:app --reload`, then
`curl -s localhost:8000/v1/chat -H 'content-type: application/json' -d '{"message":"veg starters under 250 in Gachibowli"}'`

## Layout

| Path | What it does |
| --- | --- |
| `scripts/schema.sql` | Tables + indexes. Vector size (384) must match `EMBEDDING_DIM` |
| `scripts/seed_data.py` | Fake restaurants and dishes |
| `app/search.py` | `search_dishes()` — filters + vector rank + grouping |
| `app/llm.py` | Claude tool loop, system prompt, crude price grounding check |
| `chat.py` | Terminal chat |
| `app/main.py` | FastAPI `/v1/chat` (in-memory sessions, dev only) |
| `eval/search_cases.json` | Search test cases; add one for every bad result you find |

## Next steps

1. Replace fake data with 20–30 real restaurants from one neighborhood (hand-entered first).
2. Test the embedding model on your real queries, including Telugu/Hindi; swap model + `EMBEDDING_DIM` + schema together if needed.
3. Add an LLM-level eval (30 chat queries, check answers cite only returned dishes).
4. Streaming + a one-page web UI with result cards.
5. Then owner updates (auth, preview, confirm, audit log).

## Known gaps

- `hours` / open-now filtering is not implemented.
- Area must match exactly (case-insensitive); Claude maps user wording to the known-areas list in the prompt.
- Grounding check only compares ₹ prices, and only prints a warning.
- No auth, rate limiting or persistence for API sessions.
- Check the current Claude model name in Anthropic's docs; `CLAUDE_MODEL` is set in `.env`.
