from fastapi import FastAPI, Query
from database import SessionLocal
from crud import get_top_products, get_channel_activity, search_messages

app = FastAPI(title="Analytical API")

@app.get("/api/reports/top-products")
def top_products(limit: int = 10):
    return get_top_products(limit)

@app.get("/api/channels/{channel_name}/activity")
def channel_activity(channel_name: str):
    return get_channel_activity(channel_name)

@app.get("/api/search/messages")
def search_messages_endpoint(query: str = Query(...)):
    return search_messages(query)
