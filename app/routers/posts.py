from typing import List

from fastapi import APIRouter, HTTPException, status

from app import storage
from app.models import PostCreate, PostOut, PostUpdate

router = APIRouter()


@router.post("/posts", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post_endpoint(payload: PostCreate) -> PostOut:
    async with storage.lock:
        author = await storage.get_user(payload.authorId)
        if not author:
            raise HTTPException(status_code=400, detail="author not found")
        post = await storage.create_post(payload.dict())
        await storage.save_to_file()
        return PostOut(**post)


@router.get("/posts", response_model=List[PostOut])
async def list_posts_endpoint() -> List[PostOut]:
    posts = await storage.list_posts()
    return [PostOut(**p) for p in posts]


@router.get("/posts/{post_id}", response_model=PostOut)
async def get_post_endpoint(post_id: int) -> PostOut:
    post = await storage.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return PostOut(**post)


@router.put("/posts/{post_id}", response_model=PostOut)
async def update_post_endpoint(post_id: int, payload: PostUpdate) -> PostOut:
    async with storage.lock:
        post = await storage.update_post(post_id, payload.dict())
        if not post:
            raise HTTPException(status_code=404, detail="post not found")
        await storage.save_to_file()
        return PostOut(**post)


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_endpoint(post_id: int) -> None:
    async with storage.lock:
        removed = await storage.delete_post(post_id)
        if not removed:
            raise HTTPException(status_code=404, detail="post not found")
        await storage.save_to_file()
