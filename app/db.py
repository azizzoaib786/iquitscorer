import os
import boto3
from boto3.dynamodb.conditions import Key
from typing import Any, Dict, List, Optional

# AWS configuration
AWS_REGION = os.getenv("AWS_REGION", "me-central-1")
GAMES_TABLE = os.getenv("GAMES_TABLE", "iquit_games")
EVENTS_TABLE = os.getenv("EVENTS_TABLE", "iquit_events")

ddb = boto3.resource("dynamodb", region_name=AWS_REGION)
games = ddb.Table(GAMES_TABLE)
events = ddb.Table(EVENTS_TABLE)


def put_game(item: Dict[str, Any]) -> None:
    # Create new game
    games.put_item(Item=item)


def get_game(game_id: str) -> Optional[Dict[str, Any]]:
    # Get game by ID
    resp = games.get_item(Key={"game_id": game_id})
    return resp.get("Item")


def list_games(limit: int = 20) -> List[Dict[str, Any]]:
    # List recent games
    resp = games.scan(Limit=limit)
    items = resp.get("Items", [])
    items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return items


def update_game(game_id: str, update_expr: str, expr_vals: Dict[str, Any]) -> None:
    # Update game attributes
    games.update_item(
        Key={"game_id": game_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_vals,
    )


def list_events(game_id: str) -> List[Dict[str, Any]]:
    # Get all scoring events
    resp = events.query(
        KeyConditionExpression=Key("game_id").eq(game_id),
        ScanIndexForward=True,
    )
    return resp.get("Items", [])


def put_event(item: Dict[str, Any]) -> None:
    # Record scoring event
    events.put_item(Item=item)


def mark_event_undone(game_id: str, ts: str, undone: bool) -> None:
    # Mark event as undone
    events.update_item(
        Key={"game_id": game_id, "ts": ts},
        UpdateExpression="SET undone = :u",
        ExpressionAttributeValues={":u": undone},
    )