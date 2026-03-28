from collections import defaultdict
from typing import Dict, List, Optional


def totals_by_player(players: List[str], events: List[dict]) -> Dict[str, int]:
    # Sum all deltas per player
    totals = {p: 0 for p in players}
    for e in events:
        if e.get("undone"):
            continue
        p = e["player"]
        totals[p] = totals.get(p, 0) + int(e["delta"])
    return totals


def get_out_timestamps(events: List[dict], players: List[str], target: int) -> Dict[str, Optional[str]]:
    # Find timestamp when each player went OUT (reached target)
    out_ts: Dict[str, Optional[str]] = {p: None for p in players}
    running_totals: Dict[str, int] = {p: 0 for p in players}
    
    # Events are sorted by timestamp
    for e in events:
        if e.get("undone"):
            continue
        
        player = e["player"]
        running_totals[player] += int(e["delta"])
        
        # Record first timestamp when player reaches target
        if out_ts[player] is None and running_totals[player] >= target:
            out_ts[player] = e["ts"]
    
    return out_ts


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


def leaderboard(players: List[str], totals: Dict[str, int], target: int, events: List[dict] = None) -> List[dict]:
    # Generate ranked leaderboard
    # Calculate out timestamps if events provided
    out_timestamps = {}
    if events:
        out_timestamps = get_out_timestamps(events, players, target)
    
    rows = []
    for p in players:
        t = int(totals.get(p, 0))
        is_out = t >= target
        out_ts = out_timestamps.get(p) if events else None
        rows.append({
            "player": p,
            "total": t,
            "is_out": is_out,
            "out_timestamp": out_ts
        })

    # Sort active by score (lowest first)
    active = sorted([r for r in rows if not r["is_out"]], key=lambda r: r["total"])
    
    # Sort OUT players by timestamp (who went out first)
    out = sorted(
        [r for r in rows if r["is_out"]],
        key=lambda r: (r["out_timestamp"] or "", r["total"])  # Sort by timestamp, then score
    )

    # Combine and assign ranks
    ranked = active + out
    for i, r in enumerate(ranked, start=1):
        r["rank"] = i
    return ranked