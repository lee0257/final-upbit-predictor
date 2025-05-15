import requests
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def fetch_upbit_data():
    # 더미 로직 (실제로는 급등 포착 알고리즘을 넣어야 함)
    return {
        "should_alert": True,
        "message": "[선행급등포착]\n- 코인명: SUI\n- 현재가: 713원\n- 매수 추천가: 705 ~ 710원\n- 목표 매도가: 735원\n- 예상 수익률: 3.5%\n- 예상 소요 시간: 7분\n- 추천 이유: 체결량 급증 + 매수 강세 포착",
        "symbol": "SUI",
        "price": 713
    }

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=payload)

def save_to_supabase(data):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"symbol": data["symbol"], "price": data["price"]}
    requests.post(f"{SUPABASE_URL}/rest/v1/predictions", json=payload, headers=headers)
