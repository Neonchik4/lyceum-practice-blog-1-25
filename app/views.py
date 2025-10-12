from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import Response

from app import storage

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def home(request: Request) -> Response:
    posts = await storage.list_posts()
    posts_sorted = sorted(posts, key=lambda p: p["createdAt"], reverse=True)
    posts_with_author = []
    for p in posts_sorted:
        author = await storage.get_user(p["authorId"])
        p_copy = p.copy()
        p_copy["authorLogin"] = author["login"] if author else "Неизвестно"
        posts_with_author.append(p_copy)
    return templates.TemplateResponse(
        "home.html", {"request": request, "posts": posts_with_author}
    )


@router.get("/posts/new")
async def new_post_form(request: Request) -> Response:
    users = await storage.list_users()
    return templates.TemplateResponse(
        "post_form.html", {"request": request, "users": users, "action": "/posts/new"}
    )


@router.post("/posts/new")
async def create_post_form(
    title: str = Form(...), content: str = Form(...), authorId: int = Form(...)
) -> RedirectResponse:
    async with storage.lock:
        author = await storage.get_user(authorId)
        if not author:
            return RedirectResponse(url="/posts/new", status_code=303)
        await storage.create_post(
            {"title": title, "content": content, "authorId": authorId}
        )
        await storage.save_to_file()
    return RedirectResponse(url="/", status_code=303)


@router.get("/posts/{post_id}")
async def view_post(request: Request, post_id: int) -> Response:
    post = await storage.get_post(post_id)
    if not post:
        return RedirectResponse(url="/", status_code=303)
    author = await storage.get_user(post["authorId"])
    return templates.TemplateResponse(
        "post_view.html", {"request": request, "post": post, "author": author}
    )


@router.get("/posts/{post_id}/edit")
async def edit_post_form(request: Request, post_id: int) -> Response:
    post = await storage.get_post(post_id)
    if not post:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse(
        "post_form.html",
        {
            "request": request,
            "post": post,
            "users": await storage.list_users(),
            "action": f"/posts/{post_id}/edit",
        },
    )


@router.post("/posts/{post_id}/edit")
async def edit_post(
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    authorId: int = Form(...),
) -> RedirectResponse:
    async with storage.lock:
        p = await storage.update_post(
            post_id, {"title": title, "content": content, "authorId": authorId}
        )
        if not p:
            return RedirectResponse(url="/", status_code=303)
        await storage.save_to_file()
    return RedirectResponse(url=f"/posts/{post_id}", status_code=303)


@router.post("/posts/{post_id}/delete")
async def delete_post_form(post_id: int) -> RedirectResponse:
    async with storage.lock:
        removed = await storage.delete_post(post_id)
        if removed is None:
            await storage.save_to_file()
            return RedirectResponse(url="/", status_code=303)
        posts_items = sorted(storage.posts.items(), key=lambda item: int(item[0]))
        new_posts = {}
        new_id = 1
        for _, post in posts_items:
            post_copy = post.copy()
            post_copy["id"] = new_id
            new_posts[new_id] = post_copy
            new_id += 1
        storage.posts.clear()
        storage.posts.update(new_posts)
        storage.next_post_id = new_id
        await storage.save_to_file()
    return RedirectResponse(url="/", status_code=303)


@router.get("/users/new")
async def new_user_form(request: Request) -> Response:
    return templates.TemplateResponse(
        "user_form.html", {"request": request, "action": "/users/new"}
    )


@router.post("/users/new")
async def create_user_form(
    email: str = Form(...), login: str = Form(...), password: str = Form(...)
) -> RedirectResponse:
    async with storage.lock:
        await storage.create_user(
            {"email": email, "login": login, "password": password}
        )
        await storage.save_to_file()
    return RedirectResponse(url="/", status_code=303)
