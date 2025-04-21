CREATE TABLE media_notes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    author TEXT,
    category TEXT CHECK (category IN ('Cinema', 'Book', 'Song')) NOT NULL,
    status TEXT CHECK (status IN ('planned', 'done')) DEFAULT 'planned'
);
