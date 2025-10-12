import asyncio
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

# -----------------------
# Глобальные переменные
# -----------------------
users: Dict[int, Dict[str, Any]] = {}
posts: Dict[int, Dict[str, Any]] = {}
next_user_id: int = 1
next_post_id: int = 1

# путь к файлу хранения
store_dir = os.path.join(os.getcwd(), "data")
store_path = os.path.join(store_dir, "store.json")

# asyncio Lock для безопасности при записи/чтении
lock: asyncio.Lock = asyncio.Lock()


# -----------------------
# Вспомогательные функции
# -----------------------
def _now_iso() -> str:
    return datetime.utcnow().isoformat()


# -----------------------
# Работа с файлом
# -----------------------
async def load_from_file() -> None:
    global users, posts, next_user_id, next_post_id
    os.makedirs(store_dir, exist_ok=True)
    if not os.path.exists(store_path):
        return

    async with lock:
        with open(store_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            users = {int(k): v for k, v in data.get("users", {}).items()}
            posts = {int(k): v for k, v in data.get("posts", {}).items()}
            next_user_id = data.get("next_user_id", 1)
            next_post_id = data.get("next_post_id", 1)


async def save_to_file() -> None:
    async with lock:
        os.makedirs(store_dir, exist_ok=True)
        data = {
            "users": users,
            "posts": posts,
            "next_user_id": next_user_id,
            "next_post_id": next_post_id,
        }
        with open(store_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


# -----------------------
# CRUD для пользователей
# -----------------------
async def create_user(payload: Dict[str, Any]) -> Dict[str, Any]:
    global next_user_id
    uid = next_user_id
    next_user_id += 1
    users[uid] = {**payload, "id": uid, "createdAt": _now_iso()}
    await save_to_file()
    return users[uid]


async def get_user(uid: int) -> Optional[Dict[str, Any]]:
    return users.get(uid)


async def list_users() -> List[Dict[str, Any]]:
    return list(users.values())


async def update_user(uid: int, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    user = users.get(uid)
    if not user:
        return None
    users[uid].update(payload)
    await save_to_file()
    return users[uid]


async def delete_user(uid: int) -> Optional[Dict[str, Any]]:
    removed = users.pop(uid, None)
    if removed:
        await save_to_file()
    return removed


# -----------------------
# CRUD для постов
# -----------------------
async def create_post(payload: Dict[str, Any]) -> Dict[str, Any]:
    global next_post_id
    pid = next_post_id
    next_post_id += 1
    posts[pid] = {**payload, "id": pid, "createdAt": _now_iso()}
    await save_to_file()
    return posts[pid]


async def get_post(pid: int) -> Optional[Dict[str, Any]]:
    return posts.get(pid)


async def list_posts() -> List[Dict[str, Any]]:
    return list(posts.values())


async def update_post(pid: int, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    post = posts.get(pid)
    if not post:
        return None
    posts[pid].update(payload)
    await save_to_file()
    return posts[pid]


async def delete_post(pid: int) -> Optional[Dict[str, Any]]:
    removed = posts.pop(pid, None)
    if removed:
        await save_to_file()
    return removed
