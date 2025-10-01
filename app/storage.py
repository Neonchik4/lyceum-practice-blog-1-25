import json
from datetime import datetime
from typing import Dict, Any
import os
import asyncio

store_path = "app/data/store.json"
users: Dict[int, Dict[str, Any]] = {}
posts: Dict[int, Dict[str, Any]] = {}
next_user_id = 1
next_post_id = 1

def _now_iso():
    return datetime.utcnow().isoformat()

async def load_from_file():
    global users, posts, next_user_id, next_post_id
    if not os.path.exists(store_path):
        with open(store_path, "w", encoding="utf-8") as f:
            json.dump({}, f)
        users = {}
        posts = {}
        next_user_id = 1
        next_post_id = 1
        return
    try:
        with open(store_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}
    raw_users = data.get("users") or {}
    raw_posts = data.get("posts") or {}
    users = {int(k): v for k, v in raw_users.items()}
    posts = {int(k): v for k, v in raw_posts.items()}
    if users:
        next_user_id = max(users.keys()) + 1
    else:
        next_user_id = int(data.get("next_user_id", 1))
    if posts:
        next_post_id = max(posts.keys()) + 1
    else:
        next_post_id = int(data.get("next_post_id", 1))

async def save_to_file():
    tmp_path = store_path + ".tmp"
    data = {
        "users": users,
        "posts": posts,
        "next_user_id": next_user_id,
        "next_post_id": next_post_id
    }
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, store_path)

async def create_user(payload: dict):
    global next_user_id
    uid = next_user_id
    next_user_id += 1
    now = _now_iso()
    users[uid] = {
        "id": uid,
        "email": payload["email"],
        "login": payload["login"],
        "password": payload["password"],
        "createdAt": now,
        "updatedAt": now
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
    return users.pop(uid, None)

async def create_post(payload: dict):
    global next_post_id
    pid = next_post_id
    next_post_id += 1
    now = _now_iso()
    posts[pid] = {
        "id": pid,
        "authorId": payload["authorId"],
        "title": payload["title"],
        "content": payload["content"],
        "createdAt": now,
        "updatedAt": now
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
    return posts.pop(pid, None)
