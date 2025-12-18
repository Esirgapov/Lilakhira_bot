from aiosqlite import connect

async def create_db():
    async with connect('database.db') as db:
        await db.execute(
            'CREATE TABLE IF NOT EXISTS users ('
            'user_id INTEGER PRIMARY KEY, '
            'first_name TEXT, '
            'last_name TEXT, '
            'phone TEXT)'
        )
        await db.commit()


async def init_db():
    async with connect("database.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                location TEXT,
                time TEXT,
                orientir TEXT,
                metro TEXT,
                link TEXT,
                image TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                event_id INTEGER
            )
        """)
        await db.commit()

