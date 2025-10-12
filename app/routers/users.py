from typing import Any, Dict, List, Optional

from fastapi import APIRouter

from app import storage

router = APIRouter()


@router.get("/users/{user_id}")
async def get_user_endpoint(user_id: int) -> Optional[Dict[str, Any]]:
    return await storage.get_user(user_id)


@router.get("/users", response_model=List[Dict[str, Any]])
async def list_users_endpoint() -> List[Dict[str, Any]]:
    return await storage.list_users()
