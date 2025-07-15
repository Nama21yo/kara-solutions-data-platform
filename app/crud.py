from database import SessionLocal

def get_top_products(limit: int):
    db = SessionLocal()
    res = db.execute("""
        SELECT product_name, COUNT(*) as mentions
        FROM fct_messages
        GROUP BY product_name
        ORDER BY mentions DESC
        LIMIT :limit
    """, {"limit": limit})
    return [dict(r) for r in res]

def get_channel_activity(channel_name: str):
    db = SessionLocal()
    res = db.execute("""
        SELECT date_trunc('day', created_at) as day, COUNT(*) as posts
        FROM fct_messages
        WHERE channel_name = :ch
        GROUP BY day ORDER BY day
    """, {"ch": channel_name})
    return [dict(r) for r in res]

def search_messages(query: str):
    db = SessionLocal()
    res = db.execute("""
        SELECT message_id, content
        FROM fct_messages
        WHERE content ILIKE '%' || :q || '%'
    """, {"q": query})
    return [dict(r) for r in res]
