from flask import Flask
import threading
import time
from datetime import datetime, timedelta
from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import numpy as np
import pytz
import time
import requests
from datetime import datetime, timedelta
ist = pytz.timezone('Asia/Kolkata')
tv = TvDatafeed("mekalaganeshreddy796", "Ganesh?!1")
app = Flask(__name__)
running = False
thread = None
def my_function():
  length=500
  countlimit=length
  taken=0
  triggered = 0
  total_profit = 0
  total_loss = 0
  net_profit = 0
  current_profit = 0
  countCandles=0
  flag=True
  eachamount=7000
  sumofselltobuy=[]
  l=[]
  g=0
  d=-1
  reversefalse=False
  hdfc = tv.get_hist(symbol='HDFCBANK', exchange='NSE', interval=Interval.in_15_minute, n_bars=length)
  banknifty = tv.get_hist(symbol='BANKNIFTY', exchange='NSE', interval=Interval.in_15_minute, n_bars=length)
  banknifty = banknifty.tz_localize('UTC').tz_convert('Asia/Kolkata')
  banknifty_datetime = banknifty.index[g:d].tolist()
  hdfc_close_list = hdfc['close'][g:d].tolist()
  hdfc_open_list = hdfc['open'][g:d].tolist()
  hdfc_volume_list = hdfc['volume'][g:d].tolist()
  hdfc_high_list = hdfc['high'][g:d].tolist()
  hdfc_low_list = hdfc['low'][g:d].tolist()
  banknifty_close_list = banknifty['close'][g:d].tolist()
  banknifty_open_list = banknifty['open'][g:d].tolist()
  banknifty_high_list = banknifty['high'][g:d].tolist()
  banknifty_low_list = banknifty['low'][g:d].tolist()
  banknifty_volume_list = banknifty['volume'][g:d].tolist()
  entry_price = None
  position_type = None
  loss_threshold = 20
  reversal_count = 0
  max_reversals = 2
  max_profit_points = 500
  max_loss_points = 150
  k=None
  store=None
  take_profit_pct = 0.01
  entrydate=None
  entrytime=None
  trade_data = []
  demo_trade=[]
  j=0

  for i in range(15,len(hdfc_close_list)):
      current_time = banknifty_datetime[i]
      current_date_str = current_time.strftime("%Y-%m-%d")

      day_of_week = datetime.strptime(current_date_str, "%Y-%m-%d").strftime("%A")

      current_time_str = current_time.strftime("%H:%M")

      hour = current_time_str.split(":")[0]
      if  current_time_str == "09:15":
        flag=False
      if current_time_str == "15:00":
          if position_type:
              exit_price = hdfc_close_list[i]
              if position_type == 'buy':
                  trade_profit = exit_price - entry_price
              else:
                  trade_profit = entry_price - exit_price
              if trade_profit >= 0:
                  total_profit += trade_profit
              else:
                  total_loss += abs(trade_profit)
              net_profit = total_profit - total_loss
              s=((trade_profit)*100*5/hdfc_close_list[i])
              l.append(s)
             
              demo_trade.append({  'symbol': 'HDFC','Date': entrydate,'Position_Type': position_type,'Time':current_time_str,'Exit_Price':exit_price})
      
              triggered += 1
              flag=False
              position_type = None
              entry_price = None
              reversal_count = 0
              current_profit = 0
          continue
      all_buy = (
          hdfc_close_list[i] > hdfc_open_list[i]
      )
      all_sell = (
        hdfc_close_list[i] < hdfc_open_list[i]
      )
      if (hdfc_volume_list[i])>150000 and hdfc_volume_list[i]<1700000:
        flag=True

      if all_buy and flag and position_type != 'buy':

        if position_type == 'sell'  :
            exit_price = hdfc_close_list[i]
            trade_profit = entry_price - exit_price
            if trade_profit >= 0:
                total_profit += trade_profit
            else:
                total_loss += abs(trade_profit)
            net_profit = total_profit - total_loss
            s=((trade_profit)*100/hdfc_close_list[i])
            l.append(s)

            demo_trade.append({  'symbol': 'HDFC','Date': entrydate,'Position_Type': position_type,'Time':current_time_str,'Exit_Price':exit_price})
  
            position_type = None
            entry_price = None
            triggered += 1
        if  current_time_str != "15:00"  and current_time_str != "15:15" :
            countlimit=14
            countCandles=0
            taken+=1
            entrydate=current_date_str
            entrytime=current_time_str
            flag=False

            position_type = 'buy'
            reversefalse=False
            entry_price = hdfc_close_list[i]
            reversal_count = 0
            current_profit = 0
      if all_sell and flag  and position_type != 'sell':
          if position_type == 'buy':
              exit_price = hdfc_close_list[i]
              trade_profit = exit_price - entry_price
              if trade_profit >= 0:
                  total_profit += trade_profit
              else:
                  total_loss += abs(trade_profit)
              net_profit = total_profit - total_loss
              s=(int(trade_profit)*5*100/1800)
              l.append(s)
              eachamount += eachamount * (s / 100)
              demo_trade.append({  'symbol': 'HDFC','Date': entrydate,'Position_Type': position_type,'Time':current_time_str,'Exit_Price':exit_price})
     
              position_type = None
              entry_price = None
              triggered += 1
          if  current_time_str != "15:00"    and current_time_str != "15:15"  :
              countlimit=13
              countCandles=0
              taken+=1
              k= banknifty_open_list[i]
              demo_trade.append({  'symbol': 'HDFC','Date': entrydate,'Position_Type': position_type,'Time':current_time_str,'Entry_Price':entry_price})
      
              entrydate=current_date_str
              entrytime=current_time_str
              reversefalse=False
              flag=False
              entry=banknifty_close_list[0]
              position_type = 'sell'
              entry_price = hdfc_close_list[i]
              reversal_count = 0
              current_profit = 0

  last_trade = demo_trade[-1]
  print(demo_trade[-1])
  last_trade_time_str = last_trade.get('Time') 
  last_trade_Date_str = last_trade.get('Date') 

  # Combine date and time from last trade
  last_trade_datetime = datetime.strptime(f"{last_trade_Date_str} {last_trade_time_str}", "%Y-%m-%d %H:%M")
  india_timezone = pytz.timezone('Asia/Kolkata')
  last_trade_datetime = india_timezone.localize(last_trade_datetime)

  # Current time
  now = datetime.now(india_timezone)

  # Difference in seconds
  diff_seconds = (now - last_trade_datetime).total_seconds()
  diff_seconds = 0
  print("Difference in seconds:", diff_seconds)

    # Check if the difference is less than 2 minutes
  if  diff_seconds < 200:
        lasttrade_list = last_trade.keys()
        if 'Entry_Price' in lasttrade_list:

          Position_send_to_firebase(last_trade)
          bot_token = '7747497929:AAHPFWQ3G-59BtozjVPN4Qqpu4qux4TP-WE'         # Replace with your bot token
          chat_id = '1608202016'             # Replace with your chat ID
          message = f"New Entry :  {last_trade['symbol']} {last_trade['Position_Type']} at {last_trade['Entry_Price']} on {last_trade['Date']} {last_trade['Time']}" # Changed here to directly access the keys from last_trade dictionary

          url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
          params = {'chat_id': chat_id, 'text': message}

          response = requests.get(url, params=params)
          print(response.json())
        if 'Exit_Price' in lasttrade_list:


          bot_token = '7747497929:AAHPFWQ3G-59BtozjVPN4Qqpu4qux4TP-WE'
          chat_id = '1608202016'             # Replace with your chat ID
          message = f"New Exit :  {last_trade['symbol']} {last_trade['Position_Type']} at {last_trade['Exit_Price']} on {last_trade['Date']} {last_trade['Time']}" # Changed here to directly access the keys from last_trade dictionary
          url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
          params = {'chat_id': chat_id, 'text': message}

          response = requests.get(url, params=params)
          print(response.json())


def is_trading_time():
    now = datetime.now()
    # Monday=0 … Sunday=6
    if now.weekday() >= 5:  # Sat or Sun
        return False
    return 9 <= now.hour < 16  # 9:00–15:59

def wait_for_next_15min_mark():
    print("📌 Trading thread started")
    while True:
        if not is_trading_time():
            print("⏸ Outside trading hours, sleeping 60s...")
            time.sleep(60)
            continue

        now = datetime.now()
        minutes_to_add = (15 - (now.minute % 15)) % 15
        if minutes_to_add == 0:
            minutes_to_add = 15

        next_mark = now.replace(second=0, microsecond=0) + timedelta(minutes=minutes_to_add)
        next_mark += timedelta(seconds=3)  # small buffer

        sleep_time = (next_mark - datetime.now()).total_seconds()
        if sleep_time > 0:
            print(f"⏳ Sleeping {int(sleep_time)}s until {next_mark.strftime('%H:%M:%S')}")
            time.sleep(sleep_time)

        if is_trading_time():
            print(f"🚀 Running my_function() at {datetime.now().strftime('%H:%M:%S')}")
            my_function()

@app.route("/")
def home():
    return "✅ Render alive. Trading runs Mon–Fri, 9AM–4PM every 15m."

def start_background():
    thread = threading.Thread(target=wait_for_next_15min_mark, daemon=True)
    thread.start()

if __name__ == "__main__":
    start_background()  # 👈 automatically starts when app boots
    app.run(host="0.0.0.0", port=5000)
