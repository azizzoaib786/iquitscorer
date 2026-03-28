import os
import boto3
from boto3.dynamodb.conditions import Key
from typing import Any, Dict, List, Optional

# AWS configuration
AWS_REGION = os.getenv("AWS_REGION", "me-central-1")
GAMES_TABLE = os.getenv("GAMES_TABLE", "iquit_games")
EVENTS_TABLE = os.getenv("EVENTS_TABLE", "iquit_events")
USERS_TABLE = os.getenv("USERS_TABLE", "iquit_users")

ddb = boto3.resource("dynamodb", region_name=AWS_REGION)
games = ddb.Table(GAMES_TABLE)
events = ddb.Table(EVENTS_TABLE)
users = ddb.Table(USERS_TABLE)


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


def create_user(user_id: str, username: str, password_hash: str, is_admin: bool = False) -> None:
    # Create new user
    users.put_item(Item={
        "user_id": user_id,
        "username": username,
        "password_hash": password_hash,
        "is_admin": is_admin,
        "is_active": is_admin,  # Admins active by default, regular users inactive
    })


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    # Get user by username
    resp = users.scan(
        FilterExpression="username = :u",
        ExpressionAttributeValues={":u": username}
    )
    items = resp.get("Items", [])
    return items[0] if items else None


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    # Get user by ID
    resp = users.get_item(Key={"user_id": user_id})
    return resp.get("Item")


def list_games_by_user(user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    # List games created by user
    resp = games.scan(
        FilterExpression="user_id = :uid",
        ExpressionAttributeValues={":uid": user_id},
        Limit=limit
    )
    items = resp.get("Items", [])
    items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return items


def delete_game(game_id: str) -> None:
    # Delete game and all its events
    games.delete_item(Key={"game_id": game_id})
    # Delete all events for this game
    ev = list_events(game_id)
    for e in ev:
        events.delete_item(Key={"game_id": game_id, "ts": e["ts"]})


def update_user_password(user_id: str, new_password_hash: str) -> None:
    # Update user password
    users.update_item(
        Key={"user_id": user_id},
        UpdateExpression="SET password_hash = :ph",
        ExpressionAttributeValues={":ph": new_password_hash}
    )


def toggle_user_active(user_id: str, is_active: bool) -> None:
    # Toggle user active status
    users.update_item(
        Key={"user_id": user_id},
        UpdateExpression="SET is_active = :a",
        ExpressionAttributeValues={":a": is_active}
    )


def list_all_users() -> List[Dict[str, Any]]:
    # List all users (admin only)
    resp = users.scan()
    return resp.get("Items", [])


def delete_user(user_id: str) -> None:
    # Delete user (admin only)
    users.delete_item(Key={"user_id": user_id})
