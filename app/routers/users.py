from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status

from app import storage
from app.models import UserCreate, UserOut, UserUpdate

router = APIRouter()


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(payload: UserCreate) -> Dict[str, Any]:
    async with storage.lock:
        for u in storage.users.values():
            if u["email"] == payload.email:
                raise HTTPException(status_code=400, detail="email already exists")
            if u["login"] == payload.login:
                raise HTTPException(status_code=400, detail="login already exists")
        user = await storage.create_user(payload.dict())
        await storage.save_to_file()
        return user


@router.get("/users", response_model=List[UserOut])
async def list_users_endpoint() -> List[Dict[str, Any]]:
    return await storage.list_users()


@router.get("/users/{user_id}", response_model=UserOut)
async def get_user_endpoint(user_id: int) -> Dict[str, Any]:
    user = await storage.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@router.put("/users/{user_id}", response_model=UserOut)
async def update_user_endpoint(user_id: int, payload: UserUpdate) -> Dict[str, Any]:
    async with storage.lock:
        if payload.email:
            for uid, u in storage.users.items():
                if uid != user_id and u["email"] == payload.email:
                    raise HTTPException(status_code=400, detail="email already exists")
        if payload.login:
            for uid, u in storage.users.items():
                if uid != user_id and u["login"] == payload.login:
                    raise HTTPException(status_code=400, detail="login already exists")
        user = await storage.update_user(user_id, payload.dict())
        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        await storage.save_to_file()
        return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endpoint(user_id: int) -> None:
    async with storage.lock:
        removed = await storage.delete_user(user_id)
        if not removed:
            raise HTTPException(status_code=404, detail="user not found")
        await storage.save_to_file()
