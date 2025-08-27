from flask import Flask
from tvDatafeed import TvDatafeed, Interval
from datetime import datetime, timedelta
import pytz
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
ist = pytz.timezone('Asia/Kolkata')
tv = TvDatafeed("mekalaganeshreddy796", "Ganesh?!1")

def is_trading_time():
    now = datetime.now(ist)
    logger.info(f"Checking time: {now}, Weekday: {now.weekday()}, Hour: {now.hour}")
    if now.weekday() >= 5:
        return False
    return 9 <= now.hour < 16

def my_function():
    logger.info("Running my_function")
    try:
        hdfc = tv.get_hist(symbol='HDFCBANK', exchange='NSE', interval=Interval.in_15_minute, n_bars=10)
        logger.info(f"HDFC Data: {hdfc.head()}")
        # Simplified trading logic
        print("Trading logic executed")
    except Exception as e:
        logger.error(f"Error in my_function: {e}")

def wait_for_next_2min_mark():
    logger.info("Starting background thread")
    while True:
        if not is_trading_time():
            logger.info("Outside trading hours, sleeping 60s")
            time.sleep(60)
            continue
        now = datetime.now(ist)
        minutes_to_add = (2 - (now.minute % 2)) % 2
        if minutes_to_add == 0:
            minutes_to_add = 2
        next_mark = now.replace(second=0, microsecond=0) + timedelta(minutes=minutes_to_add)
        sleep_time = (next_mark - now).total_seconds()
        logger.info(f"Sleeping {sleep_time}s until {next_mark}")
        time.sleep(sleep_time)
        if is_trading_time():
            my_function()

@app.route("/")
def home():
    return "Render alive. Trading runs Mon–Fri, 9AM–4PM every 2m."

if __name__ == "__main__":
    import threading
    thread = threading.Thread(target=wait_for_next_2min_mark, daemon=True)
    thread.start()
    app.run(host="0.0.0.0", port=5000)
