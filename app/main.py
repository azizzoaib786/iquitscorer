import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .db import put_game, get_game, update_game, list_events, put_event, mark_event_undone, list_games
from .logic import totals_by_player, per_round_scores, leaderboard

app = FastAPI(title="I Quit Scoreboard (HTMX)")
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


def now_ts() -> str:
    # Generate unique timestamp for event ordering
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ") + "#" + uuid.uuid4().hex


def must_game(game_id: str) -> Dict[str, Any]:
    # Fetch game or raise 404
    g = get_game(game_id)
    if not g:
        raise HTTPException(status_code=404, detail="Game not found")
    return g


def round_locked(game: Dict[str, Any], round_id: str) -> bool:
    # Check if round is locked
    for r in game.get("rounds", []):
        if r["round_id"] == round_id:
            return bool(r.get("locked", False))
    raise HTTPException(status_code=404, detail="Round not found")


def compute_view(game: Dict[str, Any], selected_round_id: Optional[str] = None) -> Dict[str, Any]:
    # Calculate all game stats for display
    ev = list_events(game["game_id"])
    
    # Filter events to selected round only
    if selected_round_id:
        round_events = [e for e in ev if e.get("round_id") == selected_round_id]
        totals = totals_by_player(game.get("players", []), round_events)
    else:
        totals = totals_by_player(game.get("players", []), ev)
    
    board = leaderboard(game.get("players", []), totals, int(game["target"]))
    round_scores = per_round_scores(ev)
    return {"events": ev, "totals": totals, "board": board, "round_scores": round_scores}


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # Homepage with game history
    recent_games = list_games(limit=10)
    return templates.TemplateResponse("home.html", {
        "request": request,
        "recent_games": recent_games
    })


@app.post("/games")
def create_game(name: str = Form(...), target: int = Form(150)):
    # Create new game
    game_id = uuid.uuid4().hex
    put_game({
        "game_id": game_id,
        "name": name.strip(),
        "target": int(target),
        "players": [],
        "rounds": [],
        "created_at": now_ts(),
    })
    return RedirectResponse(f"/games/{game_id}", status_code=303)


@app.get("/games/{game_id}", response_class=HTMLResponse)
def game_page(request: Request, game_id: str, round_id: Optional[str] = None):
    game = must_game(game_id)

    selected_round_id = round_id
    if not selected_round_id and game.get("rounds"):
        selected_round_id = game["rounds"][0]["round_id"]

    view = compute_view(game, selected_round_id)

    return templates.TemplateResponse("game.html", {
        "request": request,
        "game": game,
        "selected_round_id": selected_round_id,
        **view
    })


@app.post("/games/{game_id}/players", response_class=HTMLResponse)
def add_player(request: Request, game_id: str, player_name: str = Form(...)):
    # Add player to game
    game = must_game(game_id)
    name = player_name.strip()
    if not name:
        raise HTTPException(400, "Empty name")
    
    # Check for duplicates
    if name in game.get("players", []):
        game2 = must_game(game_id)
        selected = (game2["rounds"][0]["round_id"] if game2.get("rounds") else None)
        view = compute_view(game2, selected)
        return templates.TemplateResponse("partials/round_panel.html", {
            "request": request, "game": game2, "selected_round_id": selected, **view,
            "flash": "Player already exists."
        })

    players = game.get("players", []) + [name]
    update_game(game_id, "SET players = :p", {":p": players})

    game2 = must_game(game_id)
    selected = (game2["rounds"][0]["round_id"] if game2.get("rounds") else None)
    view = compute_view(game2, selected)
    return templates.TemplateResponse("partials/round_panel.html", {
        "request": request, "game": game2, "selected_round_id": selected, **view,
        "flash": "Player added."
    })


@app.post("/games/{game_id}/rounds", response_class=HTMLResponse)
def add_round(request: Request, game_id: str, round_name: str = Form(...)):
    game = must_game(game_id)
    rn = round_name.strip()
    if not rn:
        raise HTTPException(400, "Empty round name")

    rid = uuid.uuid4().hex[:10]
    rounds = game.get("rounds", []) + [{"round_id": rid, "name": rn, "locked": False}]
    update_game(game_id, "SET rounds = :r", {":r": rounds})

    game2 = must_game(game_id)
    view = compute_view(game2, rid)
    return templates.TemplateResponse("partials/round_panel.html", {
        "request": request, "game": game2, "selected_round_id": rid, **view,
        "flash": "Round added."
    })


@app.post("/games/{game_id}/rounds/select", response_class=HTMLResponse)
def select_round(request: Request, game_id: str, round_id: str = Form(...)):
    game = must_game(game_id)
    view = compute_view(game, round_id)
    return templates.TemplateResponse("partials/round_panel.html", {
        "request": request, "game": game, "selected_round_id": round_id, **view
    })


@app.post("/games/{game_id}/rounds/toggle-lock", response_class=HTMLResponse)
def toggle_lock(request: Request, game_id: str, round_id: str = Form(...)):
    game = must_game(game_id)
    rounds = game.get("rounds", [])
    found = False
    for r in rounds:
        if r["round_id"] == round_id:
            r["locked"] = not bool(r.get("locked", False))
            found = True
            break
    if not found:
        raise HTTPException(404, "Round not found")

    update_game(game_id, "SET rounds = :r", {":r": rounds})

    game2 = must_game(game_id)
    view = compute_view(game2, round_id)
    return templates.TemplateResponse("partials/round_panel.html", {
        "request": request, "game": game2, "selected_round_id": round_id, **view,
        "flash": "Round lock updated."
    })


@app.post("/games/{game_id}/rounds/end", response_class=HTMLResponse)
def end_round(request: Request, game_id: str, round_id: str = Form(...)):
    # End round and lock it
    game = must_game(game_id)
    rounds = game.get("rounds", [])
    found = False
    for r in rounds:
        if r["round_id"] == round_id:
            r["locked"] = True
            found = True
            break
    if not found:
        raise HTTPException(404, "Round not found")

    update_game(game_id, "SET rounds = :r", {":r": rounds})

    game2 = must_game(game_id)
    view = compute_view(game2, round_id)
    
    # Check if all players are out
    all_out = all(entry["is_out"] for entry in view["board"])
    flash_msg = "Round ended and locked." + (" 🎉 Game Over! All players are out!" if all_out else "")
    
    return templates.TemplateResponse("partials/round_panel.html", {
        "request": request, "game": game2, "selected_round_id": round_id, **view,
        "flash": flash_msg
    })


@app.post("/games/{game_id}/scores", response_class=HTMLResponse)
def add_score(request: Request, game_id: str,
              round_id: str = Form(...),
              player: str = Form(...),
              delta: int = Form(...)):
    # Add score delta to player
    game = must_game(game_id)

    if player not in game.get("players", []):
        raise HTTPException(400, "Unknown player")

    if round_locked(game, round_id):
        raise HTTPException(409, "Round is locked")

    put_event({
        "game_id": game_id,
        "ts": now_ts(),
        "round_id": round_id,
        "player": player,
        "delta": int(delta),
        "undone": False
    })

    game2 = must_game(game_id)
    view = compute_view(game2, round_id)
    
    # Auto-detect game over
    all_out = all(entry["is_out"] for entry in view["board"])
    flash_msg = None
    if all_out:
        flash_msg = "🎉 Game Over! All players reached the target!"
    
    return templates.TemplateResponse("partials/round_panel.html", {
        "request": request, "game": game2, "selected_round_id": round_id, **view,
        "flash": flash_msg
    })


@app.post("/games/{game_id}/undo", response_class=HTMLResponse)
def undo(request: Request, game_id: str, round_id: Optional[str] = Form(None)):
    must_game(game_id)
    ev = list_events(game_id)

    undone_one = False
    for e in reversed(ev):
        if not e.get("undone"):
            mark_event_undone(game_id, e["ts"], True)
            undone_one = True
            break

    game2 = must_game(game_id)

    selected = round_id
    if not selected and game2.get("rounds"):
        selected = game2["rounds"][0]["round_id"]

    view = compute_view(game2, selected)

    return templates.TemplateResponse("partials/round_panel.html", {
        "request": request, "game": game2, "selected_round_id": selected, **view,
        "flash": ("Undone last action." if undone_one else "Nothing to undo.")
    })