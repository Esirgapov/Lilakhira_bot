from aiosqlite import connect


async def add_event(name, location, time, orientir, metro, link, image):
    async with connect("database.db") as db:
        await db.execute(
            "INSERT INTO events (name, location, time, orientir, metro, link, image) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, location, time, orientir, metro, link, image)
        )
        await db.commit()

async def get_events():
    async with connect("database.db") as db:
        cursor = await db.execute("SELECT * FROM events ORDER BY id DESC")
        return await cursor.fetchall()

async def delete_event(event_id):
    async with connect("database.db") as db:
        await db.execute(
            "DELETE FROM events WHERE id = ?",
            (event_id,)
        )
        await db.commit()

async def get_event_by_id(event_id: int):
    async with connect("database"".db") as db:
        cursor = await db.execute("SELECT * FROM events WHERE id = ?", (event_id,))
        return await cursor.fetchone()
