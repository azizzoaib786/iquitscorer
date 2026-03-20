from collections import defaultdict
from typing import Dict, List


def totals_by_player(players: List[str], events: List[dict]) -> Dict[str, int]:
    # Sum all deltas per player
    totals = {p: 0 for p in players}
    for e in events:
        if e.get("undone"):
            continue
        p = e["player"]
        totals[p] = totals.get(p, 0) + int(e["delta"])
    return totals


def per_round_scores(events: List[dict]) -> Dict[str, Dict[str, int]]:
    # Calculate scores per round
    out: Dict[str, Dict[str, int]] = {}
    for e in events:
        if e.get("undone"):
            continue
        rid = e["round_id"]
        out.setdefault(rid, {})
        out[rid][e["player"]] = out[rid].get(e["player"], 0) + int(e["delta"])
    return out


def per_round_deltas(events: List[dict]) -> Dict[str, Dict[str, List[int]]]:
    # Get list of individual deltas per player per round
    out: Dict[str, Dict[str, List[int]]] = {}
    for e in events:
        if e.get("undone"):
            continue
        rid = e["round_id"]
        player = e["player"]
        delta = int(e["delta"])
        
        if rid not in out:
            out[rid] = {}
        if player not in out[rid]:
            out[rid][player] = []
        out[rid][player].append(delta)
    return out


def leaderboard(players: List[str], totals: Dict[str, int], target: int) -> List[dict]:
    # Generate ranked leaderboard
    rows = []
    for p in players:
        t = int(totals.get(p, 0))
        rows.append({"player": p, "total": t, "is_out": t >= target})

    # Sort active and OUT players
    active = sorted([r for r in rows if not r["is_out"]], key=lambda r: r["total"])
    out = sorted([r for r in rows if r["is_out"]], key=lambda r: r["total"])

    # Combine and assign ranks
    ranked = active + out
    for i, r in enumerate(ranked, start=1):
        r["rank"] = i
    return ranked