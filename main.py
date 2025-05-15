import time
from utils import send_telegram_message, fetch_upbit_data, save_to_supabase

if __name__ == "__main__":
    print("🚀 Starting Final Upbit Predictor...")
    data = fetch_upbit_data()
    if data["should_alert"]:
        send_telegram_message(data["message"])
    save_to_supabase(data)
    time.sleep(3)
