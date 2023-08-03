import asyncpg


class Cart:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def create_cart_table_if_not_exists(self):
        await self.connector.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                user_id BIGINT,
                
                product_id INTEGER,
                product_name TEXT,
                number INTEGER,
                price INTEGER,
                
                CONSTRAINT unique_user_product UNIQUE (user_id, product_id)
            )
        """)

    async def add_to_cart(self, user_id: int, product_id: int, product_name: str, number: int, price: int):
        await self.connector.execute("""
            INSERT INTO cart (user_id, product_id, product_name, number, price)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (user_id, product_id) DO UPDATE
            SET number = EXCLUDED.number
        """, user_id, product_id, product_name, number, price)

    async def get_cart(self, user_id: int):
        query = await self.connector.fetch("""
            SELECT product_name
            FROM cart
            WHERE user_id = $1
        """, user_id)
        return [row["product_name"] for row in query] or None

    async def get_id_number(self, user_id: int, product_name: str):
        product_id, number = await self.connector.fetch("""
            SELECT product_id, number
            FROM cart
            WHERE user_id = $1 AND product_name = $2
        """, user_id, product_name)
        return product_id or None, number or None

    async def get_full_cart(self, user_id: int):
        rows = await self.connector.fetch("""
            SELECT product_id, number
            FROM cart
            WHERE user_id = $1
        """, user_id)

        product_ids = [row["product_id"] for row in rows]
        numbers = [row["number"] for row in rows]
        if product_ids:
            return product_ids, numbers
        else:
            return None, None

    async def update_number(self, user_id: int, product_id: int, new_number: int):
        await self.connector.execute("""
            UPDATE cart
            SET number = $1
            WHERE user_id = $2 AND product_id = $3
        """, new_number, user_id, product_id)

    async def delete_items(self, user_id: int, product_name: str):
        await self.connector.execute("""
            DELETE FROM cart
            WHERE user_id = $1 AND product_name = $2
        """, user_id, product_name)

    async def clear_cart(self, user_id: int):
        await self.connector.execute("""
        DELETE FROM cart 
        WHERE user_id = $1
        """, user_id)
