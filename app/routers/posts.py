from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status

from app import storage
from app.models import PostCreate, PostUpdate

router = APIRouter()


@router.post(
    "/posts", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED
)
async def create_post_endpoint(payload: PostCreate) -> Dict[str, Any]:
    async with storage.lock:
        author = await storage.get_user(payload.authorId)
        if not author:
            raise HTTPException(status_code=400, detail="author not found")
        post = await storage.create_post(payload.dict())
        await storage.save_to_file()
        return post


@router.get("/posts", response_model=List[Dict[str, Any]])
async def list_posts_endpoint() -> List[Dict[str, Any]]:
    return await storage.list_posts()


@router.get("/posts/{post_id}", response_model=Dict[str, Any])
async def get_post_endpoint(post_id: int) -> Dict[str, Any]:
    post = await storage.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return post


@router.put("/posts/{post_id}", response_model=Dict[str, Any])
async def update_post_endpoint(post_id: int, payload: PostUpdate) -> Dict[str, Any]:
    async with storage.lock:
        post = await storage.update_post(post_id, payload.dict())
        if not post:
            raise HTTPException(status_code=404, detail="post not found")
        await storage.save_to_file()
        return post


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_endpoint(post_id: int) -> None:
    async with storage.lock:
        removed = await storage.delete_post(post_id)
        if not removed:
            raise HTTPException(status_code=404, detail="post not found")
        await storage.save_to_file()
