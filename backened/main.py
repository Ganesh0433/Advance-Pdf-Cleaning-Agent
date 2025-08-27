from flask import Flask
from tvDatafeed import TvDatafeed, Interval
from datetime import datetime, timedelta
import pytz
import time
import logging
import sys

app = Flask(__name__)
ist = pytz.timezone('Asia/Kolkata')
tv = TvDatafeed("mekalaganeshreddy796", "Ganesh?!1")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

logger.info("Application starting at %s", datetime.now(ist))

def is_trading_time():
    now = datetime.now(ist)
    logger.info(f"Checking time: {now}, Weekday: {now.weekday()}, Hour: {now.hour}")
    if now.weekday() >= 5:
        logger.info("Outside trading: Weekend")
        return False
    is_trading = 9 <= now.hour < 16
    logger.info(f"Is trading time: {is_trading}")
    return is_trading

def my_function():
    logger.info("Starting my_function")
    try:
        logger.info("Fetching HDFC data")
        hdfc = tv.get_hist(symbol='HDFCBANK', exchange='NSE', interval=Interval.in_15_minute, n_bars=10)
        if hdfc is None or hdfc.empty:
            logger.error("No data received for HDFCBANK")
            return
        logger.info(f"HDFC Data: {hdfc.head()}")
        logger.info("Fetching BankNIFTY data")
        banknifty = tv.get_hist(symbol='BANKNIFTY', exchange='NSE', interval=Interval.in_15_minute, n_bars=10)
        if banknifty is None or banknifty.empty:
            logger.error("No data received for BANKNIFTY")
            return
        logger.info(f"BankNIFTY Data: {banknifty.head()}")
        logger.info("Trading logic executed")
        # Add your trading logic here
    except Exception as e:
        logger.error(f"Error in my_function: {e}", exc_info=True)

def wait_for_next_2min_mark():
    logger.info("Starting background thread")
    while True:
        if not is_trading_time():
            logger.info("Outside trading hours, sleeping 60s")
            time.sleep(60)
            continue
        now = datetime.now(ist)
        logger.info(f"Current time: {now}")
        minutes_to_add = (2 - (now.minute % 2)) % 2
        if minutes_to_add == 0:
            minutes_to_add = 2
        next_mark = now.replace(second=0, microsecond=0) + timedelta(minutes=minutes_to_add)
        sleep_time = (next_mark - now).total_seconds()
        logger.info(f"Sleeping {sleep_time}s until {next_mark}")
        time.sleep(sleep_time)
        if is_trading_time():
            logger.info("Running my_function")
            my_function()

@app.route("/")
def home():
    logger.info("Home endpoint accessed")
    return "✅ Render alive. Trading runs Mon–Fri, 9AM–4PM every 2m."

@app.route("/health")
def health():
    logger.info("Health check accessed")
    return "App is running"

@app.route("/test-trading")
def test_trading():
    logger.info("Manual trigger for my_function")
    my_function()
    return "Trading logic triggered"

if __name__ == "__main__":
    logger.info("Starting Flask app")
    import threading
    thread = threading.Thread(target=wait_for_next_2min_mark, daemon=True)
    thread.start()
    app.run(host="0.0.0.0", port=5000)
