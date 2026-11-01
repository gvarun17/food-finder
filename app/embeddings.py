from functools import lru_cache

from app.config import EMBEDDING_DIM, EMBEDDING_MODEL


@lru_cache(maxsize=1)
def _model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(EMBEDDING_MODEL)


def embed(texts: list[str]) -> list[list[float]]:
    vecs = _model().encode(texts, normalize_embeddings=True, show_progress_bar=False)
    assert vecs.shape[1] == EMBEDDING_DIM, (
        f"Model returns {vecs.shape[1]} dims but EMBEDDING_DIM={EMBEDDING_DIM}; "
        "update .env and scripts/schema.sql together."
    )
    return vecs.tolist()


def embed_one(text: str) -> list[float]:
    return embed([text])[0]
