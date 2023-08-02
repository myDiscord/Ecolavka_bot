import asyncpg


class Users:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def create_users_table_if_not_exists(self):
        await self.connector.execute("""
            CREATE TABLE IF NOT EXISTS users (
            
                telegram_id BIGINT PRIMARY KEY,
                language TEXT,
                
                name TEXT,
                phone TEXT,
                
                client_id TEXT
            )
        """)

    async def add_user(self, telegram_id, language):
        await self.connector.execute("""
        INSERT INTO users (telegram_id, language) 
        VALUES ($1, $2)
        """, telegram_id, language)

    async def update_user_data(self, telegram_id, name, phone):
        await self.connector.execute("""
            UPDATE users
            SET name = $1, phone = $2
            WHERE telegram_id = $3
        """, name, phone, telegram_id)

    async def get_language(self, telegram_id):
        query = await self.connector.fetchval("""
        SELECT language 
        FROM users 
        WHERE telegram_id = $1
        """, telegram_id)
        if query:
            return query
        else:
            return None

    async def get_phone(self, telegram_id):
        query = await self.connector.fetchval("""
        SELECT phone 
        FROM users 
        WHERE telegram_id = $1
        """, telegram_id)
        if query:
            return query
        else:
            return None

    async def add_client_id(self, telegram_id: int, client_id: str):
        await self.connector.execute("""
        UPDATE users
        SET client_id = $1
        WHERE telegram_id = $2
        """, client_id, telegram_id)

    async def get_client_id(self, telegram_id: int):
        query = await self.connector.fetchval("""
        SELECT client_id 
        FROM users 
        WHERE telegram_id = $1
        """, telegram_id)

        return query or None
