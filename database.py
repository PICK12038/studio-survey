import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")


async def get_db():
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    return db


async def init_db():
    db = await get_db()
    await db.executescript("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            display_order INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class_id INTEGER NOT NULL REFERENCES classes(id),
            subjects TEXT DEFAULT '',
            is_head_teacher INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS submissions (
            id TEXT PRIMARY KEY,
            survey_code TEXT DEFAULT '',
            class_id INTEGER REFERENCES classes(id),
            teacher_id INTEGER REFERENCES teachers(id),
            created_at TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS teacher_ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_id TEXT NOT NULL REFERENCES submissions(id),
            dimension TEXT NOT NULL,
            score INTEGER NOT NULL CHECK(score BETWEEN 1 AND 10)
        );

        CREATE TABLE IF NOT EXISTS canteen_ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_id TEXT NOT NULL REFERENCES submissions(id),
            dimension TEXT NOT NULL,
            score INTEGER NOT NULL CHECK(score BETWEEN 1 AND 10)
        );

        CREATE TABLE IF NOT EXISTS dormitory_ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_id TEXT NOT NULL REFERENCES submissions(id),
            dimension TEXT NOT NULL,
            score INTEGER NOT NULL CHECK(score BETWEEN 1 AND 10)
        );

        CREATE TABLE IF NOT EXISTS suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_id TEXT NOT NULL UNIQUE REFERENCES submissions(id),
            content TEXT DEFAULT ''
        );

        CREATE INDEX IF NOT EXISTS idx_teachers_class ON teachers(class_id);
        CREATE INDEX IF NOT EXISTS idx_submissions_class ON submissions(class_id);
        CREATE INDEX IF NOT EXISTS idx_submissions_teacher ON submissions(teacher_id);
        CREATE INDEX IF NOT EXISTS idx_teacher_ratings_sub ON teacher_ratings(submission_id);
        CREATE INDEX IF NOT EXISTS idx_canteen_ratings_sub ON canteen_ratings(submission_id);
        CREATE INDEX IF NOT EXISTS idx_dormitory_ratings_sub ON dormitory_ratings(submission_id);
    """)
    await db.commit()
    await db.close()
