import asyncio
import json
import os
from datetime import datetime
from typing import Any, Dict

store_path = "app/data/store.json"
users: Dict[int, Dict[str, Any]] = {}
posts: Dict[int, Dict[str, Any]] = {}
next_user_id = 1
next_post_id = 1


def _now_iso():
    return datetime.utcnow().isoformat()


async def load_from_file():
    global users, posts, next_user_id, next_post_id
    os.makedirs(os.path.dirname(store_path), exist_ok=True)
    users = {}
    posts = {}
    next_user_id = 1
    next_post_id = 1
    with open(store_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "users": {},
                "posts": {},
                "next_user_id": next_user_id,
                "next_post_id": next_post_id,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )


async def save_to_file():
    global next_user_id, next_post_id
    os.makedirs(os.path.dirname(store_path), exist_ok=True)
    tmp_path = store_path + ".tmp"
    computed_next_user = max(users.keys()) + 1 if users else 1
    computed_next_post = max(posts.keys()) + 1 if posts else 1
    data = {
        "users": users,
        "posts": posts,
        "next_user_id": computed_next_user,
        "next_post_id": computed_next_post,
    }
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, store_path)
    next_user_id = computed_next_user
    next_post_id = computed_next_post


async def create_user(payload: dict):
    global next_user_id
    uid = max(users.keys()) + 1 if users else 1
    next_user_id = uid + 1
    now = _now_iso()
    users[uid] = {
        "id": uid,
        "email": payload["email"],
        "login": payload["login"],
        "password": payload["password"],
        "createdAt": now,
        "updatedAt": now,
    }
    return users[uid]


async def get_user(uid: int):
    return users.get(uid)


async def list_users():
    return list(users.values())


async def update_user(uid: int, payload: dict):
    user = users.get(uid)
    if not user:
        return None
    if "email" in payload and payload["email"] is not None:
        user["email"] = payload["email"]
    if "login" in payload and payload["login"] is not None:
        user["login"] = payload["login"]
    if "password" in payload and payload["password"] is not None:
        user["password"] = payload["password"]
    user["updatedAt"] = _now_iso()
    return user


async def delete_user(uid: int):
    removed = users.pop(uid, None)
    global next_user_id
    next_user_id = max(users.keys()) + 1 if users else 1
    return removed


async def create_post(payload: dict):
    global next_post_id
    pid = max(posts.keys()) + 1 if posts else 1
    next_post_id = pid + 1
    now = _now_iso()
    posts[pid] = {
        "id": pid,
        "authorId": payload["authorId"],
        "title": payload["title"],
        "content": payload["content"],
        "createdAt": now,
        "updatedAt": now,
    }
    return posts[pid]


async def get_post(pid: int):
    return posts.get(pid)


async def list_posts():
    return list(posts.values())


async def update_post(post_id: int, data: dict):
    post = posts.get(post_id)
    if not post:
        return None
    post["title"] = data.get("title", post["title"])
    post["content"] = data.get("content", post["content"])
    if "authorId" in data:
        post["authorId"] = data["authorId"]
    post["updatedAt"] = _now_iso()
    return post


async def delete_post(pid: int):
    removed = posts.pop(pid, None)
    global next_post_id
    next_post_id = max(posts.keys()) + 1 if posts else 1
    return removed
