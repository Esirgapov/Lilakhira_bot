from aiosqlite import connect

async def add_user(user_id: int, first_name: str, last_name: str, phone: str):
    async with connect('database.db') as db:
        await db.execute(
            'INSERT INTO users (user_id, first_name, last_name, phone) VALUES (?, ?, ?, ?)',
            (user_id, first_name, last_name, phone)
        )
        await db.commit()


async def get_user(user_id: int):
    async with connect('database.db') as db:
        cursor = await db.execute(
            'SELECT first_name, last_name, phone FROM users WHERE user_id = ?', (user_id,)
        )
        return await cursor.fetchone()

async def is_registered(user_id: int):
    async with connect('database.db') as db:
        cursor = await db.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
        return await cursor.fetchone() is not None


async def update_user(user_id: int, first_name: str, last_name: str, phone: str):
    async with connect('database.db') as db:
        await db.execute(
            'UPDATE users SET first_name = ?, last_name = ?, phone = ? WHERE user_id = ?',
            (first_name, last_name, phone, user_id)
        )
        await db.commit()
