"""Claude tool-use loop. Claude may only state restaurant facts that came back from search_dishes."""
import json
import re
from typing import Any

import anthropic

from app.config import CLAUDE_MODEL
from app.search import list_areas, search_dishes

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

TOOLS = [
    {
        "name": "search_dishes",
        "description": (
            "Search dishes across Hyderabad restaurants. Hard filters (area, max_price, veg_only, cuisine) "
            "are applied first, then dishes are ranked by meaning against semantic_query. "
            "Returns up to 5 restaurants with at most 2 dishes each."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "semantic_query": {
                    "type": "string",
                    "description": "What the person wants to eat, in plain words, e.g. 'spicy crispy starter' or 'mutton biryani'.",
                },
                "area": {"type": "string", "description": "Neighborhood, exactly as in the known areas list."},
                "max_price": {"type": "integer", "description": "Max price per dish in INR."},
                "veg_only": {"type": "boolean", "description": "True only if the person wants vegetarian."},
                "cuisine": {"type": "string", "description": "Optional cuisine, e.g. 'Hyderabadi', 'Chinese'."},
            },
            "required": ["semantic_query"],
        },
    }
]


def system_prompt() -> str:
    areas = ", ".join(list_areas()) or "(none loaded)"
    return f"""You help people in Hyderabad decide what to eat and where.

Rules:
- Every restaurant, dish, price and area you mention must come from a search_dishes result in this conversation. Never use your own knowledge of restaurants or menus, and never invent prices.
- If the person gave no area, ask ONE short question for it before searching, unless they said anywhere/anything.
- Known areas: {areas}. Map the person's wording to one of these; if it is not in the list, say it is not covered yet.
- Only set veg_only when they ask for vegetarian. Only set max_price when they give a budget.
- If nothing matches, say so plainly and suggest relaxing one filter (budget first). Never relax veg_only.
- Reply in the person's language. Keep it under about 120 words: 3-5 options, each as dish, restaurant, area, price in ₹, plus a few words on why it fits.
- Mention that menu data may be out of date if a result's updated_at is older than 30 days.
- Allergy questions: say menu data may be incomplete and to confirm with the restaurant."""


def _run_tool(name: str, args: dict[str, Any]) -> list[dict[str, Any]] | dict[str, str]:
    if name != "search_dishes":
        return {"error": f"unknown tool {name}"}
    allowed = {"semantic_query", "area", "max_price", "veg_only", "cuisine"}
    clean = {k: v for k, v in args.items() if k in allowed}
    results = search_dishes(**clean)
    keep = ("dish", "restaurant", "area", "price_inr", "is_veg", "spice_level", "cuisines", "phone", "updated_at", "description")
    return [{k: r[k] for k in keep} for r in results]


def _prices_in(text: str) -> set[int]:
    return {int(p) for p in re.findall(r"₹\s?(\d{2,5})", text)}


def chat_turn(messages: list[dict[str, Any]], verbose: bool = False) -> str:
    """Appends to `messages` in place and returns Claude's final text."""
    system = system_prompt()
    seen_prices: set[int] = set()

    for _ in range(5):  # hard cap on tool rounds
        resp = client.messages.create(
            model=CLAUDE_MODEL, max_tokens=1024, system=system, tools=TOOLS, messages=messages
        )
        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason != "tool_use":
            text = "".join(b.text for b in resp.content if b.type == "text")
            unknown = _prices_in(text) - seen_prices
            if unknown and seen_prices:
                # Crude grounding check: a price in the answer that no tool result contained.
                print(f"[warn] prices not found in tool results: {sorted(unknown)}")
            return text

        tool_results = []
        for block in resp.content:
            if block.type != "tool_use":
                continue
            if verbose:
                print(f"[tool] {block.name} {json.dumps(block.input, ensure_ascii=False)}")
            result = _run_tool(block.name, block.input)
            if isinstance(result, list):
                seen_prices |= {r["price_inr"] for r in result}
            tool_results.append(
                {"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(result, ensure_ascii=False, default=str)}
            )
        messages.append({"role": "user", "content": tool_results})

    return "Sorry, I couldn't finish that search. Could you rephrase?"
