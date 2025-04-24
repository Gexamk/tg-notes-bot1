CREATE TABLE IF NOT EXISTS media_notes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    author TEXT,
    category TEXT CHECK (category IN ('Cinema', 'Book', 'Song')) NOT NULL,
    status TEXT CHECK (status IN ('planned', 'done')) DEFAULT 'planned'
);


DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns 
        WHERE table_name='media_notes' AND column_name='created_at'
    ) THEN
        ALTER TABLE media_notes
        ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
    END IF;
END
$$;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL
);

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'media_notes' AND column_name = 'user_id'
    ) THEN
        ALTER TABLE media_notes
        ADD COLUMN user_id INTEGER REFERENCES users(id);
    END IF;
END
$$;


DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'users' AND column_name = 'first_name'
    ) THEN
        ALTER TABLE users
        ADD COLUMN first_name TEXT;
    END IF;
END
$$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'users' AND column_name = 'language_code'
    ) THEN
        ALTER TABLE users
        ADD COLUMN language_code TEXT;
    END IF;
END
$$;