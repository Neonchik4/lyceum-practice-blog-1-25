CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Пользователь
CREATE TABLE IF NOT EXISTS users (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255),
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Категории/тэги (tags)
CREATE TABLE IF NOT EXISTS tags (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Пост (запись блога)
CREATE TABLE IF NOT EXISTS posts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    author_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(300) NOT NULL,
    slug VARCHAR(350) NOT NULL UNIQUE,
    content TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'draft', -- draft|published|archived
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_posts_author_id ON posts(author_id);
CREATE INDEX IF NOT EXISTS idx_posts_published_at ON posts(published_at);

-- Связующая таблица пост - тэги (m:n)
CREATE TABLE IF NOT EXISTS post_tags (
    post_id uuid NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    tag_id uuid NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);

-- Список сохранённых постов (избранное)
CREATE TABLE IF NOT EXISTS favorites (
    user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    post_id uuid NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    saved_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, post_id)
);

-- Комментарии
CREATE TABLE IF NOT EXISTS comments (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id uuid NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    author_id uuid NOT NULL REFERENCES users(id) ON DELETE SET NULL,
    parent_comment_id uuid REFERENCES comments(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    is_visible BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id);

-- Подписки (user подписан на author)
CREATE TABLE IF NOT EXISTS subscriptions (
    subscriber_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    author_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (subscriber_id, author_id),
    CHECK (subscriber_id <> author_id)
);

-- Пример: триггер для обновления updated_at (опционально)
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_timestamp_on_update
BEFORE UPDATE ON posts
FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();

CREATE TRIGGER set_timestamp_on_update_users
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();
