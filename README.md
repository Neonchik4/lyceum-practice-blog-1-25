# Проект Блог
### Описание: проект на FastAPI. Позволяет смотреть блог с различными постами,создавать новых пользователей, новые посты, а также редактировать их.
## Структура проекта:
* app/
    * main.py
    * models.py
    * storage.py
    * views.py
    * data/
        * store.json
    * routers/
        * posts.py
        * users.py
    * static/
        * css/
            * base.css
            * home.css
            * post_form.css
            * post_view.css
            * user_form.css
    * templates/
        * base.html
        * home.html
        * post_form.html
        * post_view.html
        * user_form.html
* requirements.txt
* README.md
* .gitignore

## Результаты работы проекта
![]()
Главная страница выглядит так:
![](https://github.com/Neonchik4/lyceum-practice-blog-1-25/blob/master/screenshots/justBlog.png)
на ней нет постов, так как при запуске проекта JSON, в котором хранится информация по пользователям и постам, очищается.

Создание нового пользователя:
![](https://github.com/Neonchik4/lyceum-practice-blog-1-25/blob/master/screenshots/newUser.png)

Создание нового поста:

![](https://github.com/Neonchik4/lyceum-practice-blog-1-25/blob/master/screenshots/newPost.png)

Пост появляется на главной странице:

![](https://github.com/Neonchik4/lyceum-practice-blog-1-25/blob/master/screenshots/postResult.png)

Изменение поста:

![](https://github.com/Neonchik4/lyceum-practice-blog-1-25/blob/master/screenshots/changingPost.png)

![](https://github.com/Neonchik4/lyceum-practice-blog-1-25/blob/master/screenshots/changingAuthor.png)

Как видим, в посте изменился автор и содержимое:

![](https://github.com/Neonchik4/lyceum-practice-blog-1-25/blob/master/screenshots/newAuthor.png)

Также посты можно удалять (за кадром был создан ещё пост):

![](https://github.com/Neonchik4/lyceum-practice-blog-1-25/blob/master/screenshots/twoPosts.png)

Нажимаем удалить:

![](https://github.com/Neonchik4/lyceum-practice-blog-1-25/blob/master/screenshots/resOfDeleting.png)

Остается только один пост.
