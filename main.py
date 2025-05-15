
import asyncio
import websockets
import json
import requests
from datetime import datetime

SUPABASE_URL = "https://sjmdhxnvqnudjgqabsgd.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNqbWRoeG52cW51ZGpncXFic2dkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDcyODA2MTQsImV4cCI6MjA2Mjg1NjYxNH0.f8dqoeYLlAg96oImoc9rUa4gVZR9qvWdDBZdhrHZC64"

HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

async def fetch_all_krw_symbols():
    url = "https://api.upbit.com/v1/market/all"
    res = requests.get(url)
    markets = res.json()
    krw_markets = [m['market'] for m in markets if m['market'].startswith('KRW-')]
    return krw_markets

async def save_to_supabase(table, data):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    res = requests.post(url, headers=HEADERS, json=[data])
    if res.status_code >= 300:
        print(f"[ERROR] Failed to insert into {table}: {res.text}")

async def handle_message(message):
    try:
        data = json.loads(message)
        if data['ty'] == 'ticker':
            await save_to_supabase("realtime_quotes", {
                "code": data['cd'],
                "price": data['tp'],
                "volume": data['tv'],
                "timestamp": datetime.utcnow().isoformat()
            })
        elif data['ty'] == 'trade':
            await save_to_supabase("realtime_ticks", {
                "code": data['cd'],
                "price": data['tp'],
                "volume": data['tv'],
                "side": data['ab'],
                "timestamp": datetime.utcnow().isoformat()
            })
    except Exception as e:
        print(f"[ERROR] handle_message failed: {e}")

async def main():
    uri = "wss://api.upbit.com/websocket/v1"
    codes = await fetch_all_krw_symbols()

    subscribe_data = [
        {"ticket": "realtime-krw-all"},
        {"type": "ticker", "codes": codes},
        {"type": "trade", "codes": codes},
        {"format": "SIMPLE"}
    ]

    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(subscribe_data))
        print("[INFO] WebSocket connected and subscribed to all KRW markets.")

        while True:
            message = await websocket.recv()
            await handle_message(message)

if __name__ == "__main__":
    asyncio.run(main())
