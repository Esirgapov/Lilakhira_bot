from aiosqlite import connect

async def register_user(user_id, event_id):
    if await is_registered_for_event(user_id, event_id):
        return False
    async with connect("database.db") as db:
        await db.execute(
            "INSERT INTO registrations (user_id, event_id) VALUES (?, ?)",
            (user_id, event_id)
        )
        await db.commit()
    return True


async def get_registered_events(user_id: int):
    async with connect("database.db") as db:
        cursor = await db.execute("SELECT event_id FROM registrations WHERE user_id = ?", (user_id,))
        rows = await cursor.fetchall()
        return [row[0] for row in rows]
    

async def is_registered_for_event(user_id: int, event_id: int) -> bool:
    async with connect("database.db") as db:
        cursor = await db.execute(
            "SELECT id FROM registrations WHERE user_id = ? AND event_id = ?",
            (user_id, event_id)
        )
        return await cursor.fetchone() is not None
    
