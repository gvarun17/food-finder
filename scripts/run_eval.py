"""Deterministic checks on search_dishes (no LLM, no API cost): python -m scripts.run_eval

Add a case to eval/search_cases.json every time you find a bad result.
"""
import json
import sys
from collections import Counter
from pathlib import Path

from app.search import search_dishes

CASES = Path(__file__).parent.parent / "eval" / "search_cases.json"


def check(results: list[dict], checks: dict) -> list[str]:
    errs = []
    if "min_results" in checks and len(results) < checks["min_results"]:
        errs.append(f"expected >= {checks['min_results']} results, got {len(results)}")
    if "max_results" in checks and len(results) > checks["max_results"]:
        errs.append(f"expected <= {checks['max_results']} results, got {len(results)}")
    if checks.get("all_veg") and not all(r["is_veg"] for r in results):
        errs.append("non-veg dish returned for a veg request")
    if "all_max_price" in checks and any(r["price_inr"] > checks["all_max_price"] for r in results):
        errs.append("dish above max price returned")
    if "all_area" in checks and any(r["area"].lower() != checks["all_area"].lower() for r in results):
        errs.append("dish from another area returned")
    if "all_cuisine" in checks and any(checks["all_cuisine"].lower() not in [c.lower() for c in r["cuisines"]] for r in results):
        errs.append("restaurant outside requested cuisine returned")
    if "top_contains" in checks:
        top = results[:3]
        if not any(checks["top_contains"].lower() in (r["dish"] + " " + r["description"]).lower() for r in top):
            errs.append(f"no '{checks['top_contains']}' in top 3: {[r['dish'] for r in top]}")
    if "max_dishes_per_restaurant" in checks:
        if max(Counter(r["restaurant_id"] for r in results).values(), default=0) > checks["max_dishes_per_restaurant"]:
            errs.append("too many dishes from one restaurant")
    if "max_restaurants" in checks and len({r["restaurant_id"] for r in results}) > checks["max_restaurants"]:
        errs.append("too many restaurants")
    return errs


def main() -> int:
    failed = 0
    for case in json.loads(CASES.read_text()):
        results = search_dishes(
            semantic_query=case["query"], area=case.get("area"), max_price=case.get("max_price"),
            veg_only=case.get("veg_only"), cuisine=case.get("cuisine"),
        )
        errs = check(results, case["checks"])
        status = "PASS" if not errs else "FAIL"
        failed += bool(errs)
        print(f"{status}  {case['id']:<22} {len(results)} results  {[r['dish'] for r in results][:3]}")
        for e in errs:
            print(f"      - {e}")
    print(f"\n{failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
