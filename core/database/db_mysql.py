import json
from datetime import datetime
from aiomysql import connect, DictCursor


async def create_dict_con():
    connector = await connect(
        "localhost",
        "user_ecolavka",
        "=)|1+[?1KcYk1HQ1",
        "user_ecolavka",
        cursorclass=DictCursor
    )
    cursor = await connector.cursor()
    return connector, cursor


async def get_brands():
    con, cur = await create_dict_con()
    await cur.execute("""
    SELECT * 
    FROM brands
    WHERE id = 3
    """)
    query = await cur.fetchall()
    await con.ensure_closed()
    return query


async def get_lines(brand_id):
    con, cur = await create_dict_con()
    await cur.execute("""
    SELECT id, title 
    FROM brand_lines 
    WHERE brand_id = %s
    """, (brand_id,))
    query = await cur.fetchall()
    await con.ensure_closed()
    return query


async def get_categories(language, line_name):
    con, cur = await create_dict_con()
    if language == 'ru':
        if line_name == 'УХОДОВАЯ':
            await cur.execute("""
            SELECT id, title_ru
            FROM categories
            WHERE sd_id = %s
            """, ("d0_19",))
        else:
            await cur.execute("""
            SELECT id, title_ru 
            FROM categories
            WHERE title_ru LIKE %s
            """, (f"{line_name} %",))
    elif language == 'uz':
        if line_name == 'УХОДОВАЯ':
            await cur.execute("""
            SELECT id, title_uz
            FROM categories
            WHERE sd_id = %s
            """, ("d0_19",))
        else:
            await cur.execute("""
            SELECT id, title_uz 
            FROM categories
            WHERE title_uz LIKE %s
            """, (f"{line_name} %",))
    query = await cur.fetchall()
    await con.ensure_closed()
    return query


async def get_products(category_id, language):
    con, cur = await create_dict_con()
    if language == 'ru':
        await cur.execute("""
        SELECT id, title_ru, price, img 
        FROM products 
        WHERE category_id=%s
        """, (category_id, ))
    elif language == 'uz':
        await cur.execute("""
        SELECT id, title_uz, price, img 
        FROM products 
        WHERE category_id=%s
        """, (category_id, ))
    query = await cur.fetchall()
    await con.ensure_closed()
    return query


async def get_product(product_id, language):
    con, cur = await create_dict_con()
    if language == 'ru':
        await cur.execute("""
        SELECT id, title_ru, price, img 
        FROM products 
        WHERE id=%s
        """, (product_id,))
    elif language == 'uz':
        await cur.execute("""
        SELECT id, title_uz, price, img 
        FROM products 
        WHERE id=%s
        """, (product_id,))
    query = await cur.fetchone()
    await con.ensure_closed()
    return query


async def get_price(product_id, language):
    con, cur = await create_dict_con()
    if language == 'ru':
        await cur.execute("""
        SELECT price
        FROM products 
        WHERE id=%s
        """, (product_id,))
    elif language == 'uz':
        await cur.execute("""
        SELECT price
        FROM products 
        WHERE id=%s
        """, (product_id,))
    query = await cur.fetchone()
    await con.ensure_closed()
    return query


async def get_name(product_id, language):
    con, cur = await create_dict_con()
    if language == 'ru':
        await cur.execute("""
        SELECT title_ru
        FROM products 
        WHERE id=%s
        """, (product_id,))
    elif language == 'uz':
        await cur.execute("""
        SELECT title_uz
        FROM products 
        WHERE id=%s
        """, (product_id,))
    query = await cur.fetchone()
    await con.ensure_closed()
    return query


async def get_sd_id(product_id):
    con, cur = await create_dict_con()
    await cur.execute("""
    SELECT sd_id
    FROM products 
    WHERE id=%s
    """, (product_id,))
    query = await cur.fetchone()
    await con.ensure_closed()
    return query


async def get_news(language):
    con, cur = await create_dict_con()
    if language == 'ru':
        await cur.execute("""
        SELECT title_ru, id 
        FROM news 
        ORDER BY id DESC
        """)
    elif language == 'uz':
        await cur.execute("""
        SELECT title_uz, id 
        FROM news 
        ORDER BY id DESC
        """)
    query = await cur.fetchall()
    await con.ensure_closed()
    return query


async def get_post(language: str, post_id: int):
    con, cur = await create_dict_con()
    if language == 'ru':
        await cur.execute("""
        SELECT title_ru, text_ru, img 
        FROM news 
        WHERE id=%s
        """, (post_id,))
    elif language == 'uz':
        await cur.execute("""
        SELECT title_uz, text_uz, img 
        FROM news 
        WHERE id=%s
        """, (post_id,))
    query = await cur.fetchone()
    await con.ensure_closed()
    return query


async def add_order(name, phone, city, address, payment_method,
                    products, total, status, telegram_id):
    con, cur = await create_dict_con()
    await cur.execute("""
    INSERT INTO orders (name, phone, city, address, payment_method, 
        products, total, status, source, created_at, updated_at, telegram_id) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (name, phone, city, address, payment_method,
          products, total, status, 2, datetime.now(), datetime.now(), telegram_id))
    await con.commit()
    await con.ensure_closed()


async def get_history(phone, telegram_id):
    con, cur = await create_dict_con()
    await cur.execute("""
    SELECT updated_at
    FROM orders
    WHERE phone = %s OR telegram_id = %s
    ORDER BY updated_at DESC;
    """, (phone, telegram_id))
    query = await cur.fetchall()
    await con.ensure_closed()
    return query


async def get_history_order(updated_at):
    con, cur = await create_dict_con()
    await cur.execute("""
    SELECT products
    FROM orders
    WHERE updated_at = %s;
    """, (updated_at,))
    query = await cur.fetchone()
    await con.ensure_closed()
    if query is not None and 'products' in query:
        products_list = json.loads(query['products'])
    else:
        products_list = []

    return products_list
