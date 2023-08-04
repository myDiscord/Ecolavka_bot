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
        WHERE id = 3;
        """)
    query = await cur.fetchall()
    await con.ensure_closed()
    return query


async def get_lines(brand_name):
    con, cur = await create_dict_con()
    await cur.execute("""
        SELECT title
        FROM brand_lines
        WHERE title LIKE %s;
        """, (f"{brand_name}%",))
    query = await cur.fetchall()
    await con.ensure_closed()
    return query


async def get_line_id(brand_name):
    con, cur = await create_dict_con()
    await cur.execute("""
        SELECT id
        FROM brand_lines
        WHERE title LIKE %s;
        """, (f"%{brand_name}%",))
    query = await cur.fetchone()
    await con.ensure_closed()
    if query:
        return query['id']
    return None


async def get_categories(language, line_name):
    if line_name == 'УХОДОВАЯ':
        line_name = line_name.lower()
    con, cur = await create_dict_con()
    if language == 'ru':
        await cur.execute("""
        SELECT id, title_ru 
        FROM categories
        WHERE title_ru LIKE %s
        """, (f"%{line_name}%",))
    elif language == 'uz':
        await cur.execute("""
        SELECT id, title_uz 
        FROM categories
        WHERE title_uz LIKE %s
        """, (f"%{line_name}%",))
    query = await cur.fetchall()
    await con.ensure_closed()
    return query


async def get_category_id(line_name, line_id):
    if line_name == 'УХОДОВАЯ':
        line_name = line_name.lower()
    con, cur = await create_dict_con()
    await cur.execute("""
        SELECT id 
        FROM categories
        WHERE title_ru LIKE %s AND brand_line_id=%s
        """, (f"%{line_name}%", line_id))
    query = await cur.fetchone()
    await con.ensure_closed()
    if query:
        return query['id']
    return None


async def get_subcategories(language, category_id):
    con, cur = await create_dict_con()
    if language == 'ru':
        await cur.execute("""
        SELECT title_ru 
        FROM subcategories
        WHERE category_id=%s
        """, (category_id,))
    elif language == 'uz':
        await cur.execute("""
        SELECT title_uz 
        FROM subcategories
        WHERE category_id=%s
        """, (category_id,))
    query = await cur.fetchall()
    await con.ensure_closed()
    return query


async def get_subcategory_id(subcategory_name, language):
    con, cur = await create_dict_con()
    if language == 'ru':
        await cur.execute("""
            SELECT id 
            FROM subcategories
            WHERE title_ru=%s
            """, (subcategory_name,))
    elif language == 'uz':
        await cur.execute("""
            SELECT id 
            FROM subcategories
            WHERE title_uz=%s
            """, (subcategory_name,))
    query = await cur.fetchone()
    await con.ensure_closed()
    if query:
        return query['id']
    return None


async def get_products(subcategory_id, language):
    con, cur = await create_dict_con()
    if language == 'ru':
        await cur.execute("""
        SELECT title_ru
        FROM products 
        WHERE subcategory_id=%s
        """, (subcategory_id, ))
    elif language == 'uz':
        await cur.execute("""
        SELECT title_uz
        FROM products 
        WHERE subcategory_id=%s
        """, (subcategory_id,))
    query = await cur.fetchall()
    await con.ensure_closed()
    return query


async def get_product(product_name, language):
    con, cur = await create_dict_con()
    if language == 'ru':
        await cur.execute("""
        SELECT id, title_ru, price, img 
        FROM products 
        WHERE title_ru LIKE %s
        """, (f"%{product_name}%",))
    elif language == 'uz':
        await cur.execute("""
        SELECT id, title_uz, price, img 
        FROM products 
        WHERE title_uz LIKE %s
        """, (f"%{product_name}%",))
    query = await cur.fetchone()
    await con.ensure_closed()
    return query


async def get_price(product_id):
    con, cur = await create_dict_con()
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


async def get_post(language: str, title: str):
    con, cur = await create_dict_con()
    if language == 'ru':
        await cur.execute("""
        SELECT title_ru, text_ru, img 
        FROM news 
        WHERE title_ru=%s
        """, (title,))
    elif language == 'uz':
        await cur.execute("""
        SELECT title_uz, text_uz, img 
        FROM news 
        WHERE title_uz=%s
        """, (title,))
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
    return query or None


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
