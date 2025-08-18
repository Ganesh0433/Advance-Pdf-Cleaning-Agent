from flask import Flask
import firebase_admin 
from firebase_admin import credentials, firestore
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

cred = credentials.Certificate(
{
  "type": "service_account",
  "project_id": "fir-trading-72b86",
  "private_key_id": "8086214afe4c50ff4363a8ee9a50205d33cdebc4",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCrpyOWQ8v4bqnP\n5GnBQuqAMe7BYLYquTZnhiFQ6FhNbHu/uCMmOpia6u4HnS3k7NPbV3sjxhtCaDUT\n5+qgrnGXciKLOQmFltgRIBjkTsH1nZ8Yt+3xRat9CbdETxfFOn1dfYKS8k+r9TM5\nm/hH7ocn2Oox2A/uKpa4pLsK0WYfcIpd2CTbfKW6BtYlgkme7H3gon/Ig9A7/A6W\nFFHkChZAxd6w3TcMDDPmLxV7J9I+d3ZGIEdBVE+l6ZjebbNtXVTojx0AOrZpuTDd\nFPRzYmJsTW29vozaXEkq4NUlqxoa7TWIJ9FDFAe/6SlFgxUGLDL8LLf2s+BqV0nK\nTONwmCoXAgMBAAECggEAAZ3tbo5CREYmlgK8zEk+aZQO1QYoMSGAKwbPFt1ZbOvy\nA82kPHPzhAy6eUU4bXOdpe9JBak+uygSzUEzVe15Zx0iyNTyC1lvEkTkdyIWyaLW\ndiZ6uKRuB8Yo/R0RnZX+IFH9AjgDcByQgvZpJvmkOZ0yzOK6zlowWUTpTiIdfXuk\nm0XFoIhey2nySL1aE0PVV4vOaRPSFhsBMEDJNnjTvpH6+kFus2NG3BepBhuZQ70E\nt6E71dNSUKcAdIa+PJC1h0+O5DqG0pL8G9hVhzWeNdpq3BNPdFywgPl6sAPqCliN\nVBTqNztDXTsba+icUnPsRZlokL30tanRELM688a1QQKBgQDkcw38t7muwRL5bs3/\nzOrpRGIV/00pSj/ixiPeLfNxTjwsUG7F/fGSOLzBoKxYnbI5EhNJ5ko2KJ+rYOaT\n/u7O3woziUd9YExMZgtMR+9mHsBYeB6TSOtx/FPZ0mSZEuisRBgZVdKaFM7DLzPZ\npzcGay9SBI8JnqYa/2j302YEOQKBgQDAWpkgjIpLGu0Tcb2gX1BlUSG+kYyzal8F\nan1j/AQIK1NsDvuXa0eXbwcm4xIg4ixyA7Df42gJdzarVgzjc0rSVNFoK7fmv7Dk\n80KXN/emRHGx0bfx9pCM9Dmhr6OlsT2fHqOABYYE9mF0UXVJlQq2t4zPxE/q28ju\nt2psTXDAzwKBgQCxWPRp1UNr++08AJ4hUDaponG2+/wt6rtP1Fwx9mA//OlPyZ1F\nTVAFINDATHifTsT18ydQPlwsUTsrM02tZMKFjLcBrTf3iBOTV8C7ljiugX7270Fl\nO720PpvlxKReBUTlvvMqb+rPvQmKkxFgjaR08i7JMErOv//Zg6A8jDttWQKBgHxn\nm/WzL5YXmhEjVPMt8f81E8/+rrMzLrWABAzwZ2MpMlEG960c0zabtlJuNcFSxlAP\nFwwWNak5kwAJLVjFrjSOaskmzU/N1oic1AqdRewhBC9vZbp2L1MaeVObFwoIscQB\nutkHuX/oIWtra6HlZQJ7f/S4EL/i2feaZJgbFbt9AoGBAN/P6xg2kZ4RS/lOowmE\n3b1+7IEhs2o9Ly/ZxULniMgqvGtgOUdkuYNVxC2PuBd4FDluICA5p0Rm+bURtqcu\n1++BRJnqpW7LOFLDR/MPTcawSz/pwA/zl2xl1dJzyJbwwvo9/I+kBuFwapN8iNI7\n5ZMj9/o8MxzlP4StTJyTVvcc\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@fir-trading-72b86.iam.gserviceaccount.com",
  "client_id": "109754861267806926213",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40fir-trading-72b86.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
)


firebase_admin.initialize_app(cred)
db = firestore.client()


def my_function():
  length=100
  countlimit=length
  taken=0
  triggered = 0
  total_profit = 0
  total_loss = 0
  net_profit = 0
  current_profit = 0
  countCandles=0
  flag=True
  eachamount=100000
  l=[]
  d=-1

  hdfc = tv.get_hist(symbol='HDFCBANK', exchange='NSE', interval=Interval.in_15_minute, n_bars=length)
  icici = tv.get_hist(symbol='ICICIBANK', exchange='NSE', interval=Interval.in_15_minute, n_bars=length)
  sbi = tv.get_hist(symbol='SBIN', exchange='NSE', interval=Interval.in_15_minute, n_bars=length)
  axis = tv.get_hist(symbol='AXISBANK', exchange='NSE', interval=Interval.in_15_minute, n_bars=length)
  banknifty = tv.get_hist(symbol='BANKNIFTY', exchange='NSE', interval=Interval.in_15_minute, n_bars=length)
  kotak = tv.get_hist(symbol='KOTAKBANK', exchange='NSE', interval=Interval.in_15_minute, n_bars=length)
  bob = tv.get_hist(symbol='BANKBARODA', exchange='NSE', interval=Interval.in_15_minute, n_bars=length)
  banknifty = banknifty.tz_localize('UTC').tz_convert('Asia/Kolkata')

  banknifty_datetime = banknifty.index[:d].tolist()
  hdfc_close_list = hdfc['close'][:d].tolist()
  hdfc_open_list = hdfc['open'][:d].tolist()
  hdfc_high_list = hdfc['high'][:d].tolist()
  hdfc_low_list = hdfc['low'][:d].tolist()
  icici_close_list = icici['close'][:d].tolist()
  sbi_close_list = sbi['close'][:d].tolist()
  kotak_close_list = kotak['close'][:d].tolist()
  bob_close_list = bob['close'][:d].tolist()
  axis_close_list = axis['close'][:d].tolist()
  banknifty_close_list = banknifty['close'][:d].tolist()
  banknifty_open_list = banknifty['open'][:d].tolist()
  banknifty_high_list = banknifty['high'][:d].tolist()
  banknifty_low_list = banknifty['low'][:d].tolist()
  banknifty_volume_list = banknifty['volume'][:d].tolist()


  testdf=pd.DataFrame({
      'hdfc':hdfc_close_list,
      'banknifty':banknifty_datetime,

  })
  print(testdf)
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
  def Position_send_to_firebase(prediction_data):
    try:
        doc_ref = db.collection('trade_predictions').document()
        doc_ref.set({
            'symbol': prediction_data['symbol'],
            'Date': prediction_data['Date'],
            'Time': prediction_data['Time'],
            'timestamp': firestore.SERVER_TIMESTAMP,
            'Position_Type': prediction_data['Position_Type'],
            'Entry_Price': prediction_data['Entry_Price']
        })
        print("✅ Prediction sent to Firebase")
    except Exception as e:
        print(f"❌ Error sending to Firebase: {e}")
  def Exit_send_to_firebase(prediction_data):
      try:
          doc_ref = db.collection('trade_predictions').document()
          doc_ref.set({
              'symbol': prediction_data['symbol'],
              'Date': prediction_data['Date'],
              'Time': prediction_data['Time'],
              'timestamp': firestore.SERVER_TIMESTAMP,
              'Position_Type': prediction_data['Position_Type'],
              'Exit_Price': prediction_data['Exit_Price']
          })
          print("✅ Prediction sent to Firebase")
      except Exception as e:
          print(f"❌ Error sending to Firebase: {e}")
  def log_trade(serial_no, date, entry_time, exit_time, position_type, entry_price, exit_price, profit_loss, eachamount):
          nonlocal j  # Use enclosing j from my_function
          profit = exit_price - entry_price if position_type == "BUY" else entry_price - exit_price
          trade_data.append([
              serial_no + j,
              date,
              entry_time,
              exit_time,
              position_type,
              entry_price,
              exit_price,
              round(profit, 3),
              round(profit_loss, 2),
              round(eachamount, 1)
          ])
          j += 1

  df = pd.DataFrame({
      'open': banknifty_open_list,
      'close': banknifty_close_list,
      'volume': banknifty_volume_list
  })
  hdf = pd.DataFrame({
      'open': hdfc_open_list,
      'close': hdfc_close_list,

  })

  df['priceDifference'] = df['open'] - df['close']
  hdf['priceDifference'] = hdf['open'] - hdf['close']

  df['volumePriceProduct'] = ((df['volume'] * df['priceDifference']) / 50)-100000


  ma_period = 14


  df['volMA'] = df['volumePriceProduct'].rolling(window=ma_period).mean()

  df['volMA_above_zero'] = df['volMA'] + df['volume']
  for i in range(15,len(hdfc_close_list)):
      current_time = banknifty_datetime[i]
      current_time = banknifty_datetime[i]
      current_date_str = current_time.strftime("%Y-%m-%d")
      day_of_week = datetime.strptime(current_date_str, "%Y-%m-%d").strftime("%A")

      current_time_str = current_time.strftime("%H:%M")

      hour = current_time_str.split(":")[0]


      countCandles=countCandles+1

      if countCandles > countlimit:

          if position_type:
              exit_price = hdfc_close_list[i]
              if position_type == 'BUY':
                  trade_profit = exit_price - entry_price
              else:
                  trade_profit = entry_price - exit_price
              if trade_profit >= 0:
                  total_profit += trade_profit
              else:
                  total_loss += abs(trade_profit)
              net_profit = total_profit - total_loss
              s=((trade_profit)*5*100/2000)
              l.append(s)
              eachamount +=( eachamount * (s / 100))-250
              demo_trade.append({  'symbol': 'HDFC','Date': entrydate,'Position_Type': position_type,'Time':current_time_str,'Exit_Price':exit_price})
              log_trade(1, entrydate, entrytime, current_time_str, position_type, entry_price, exit_price,( eachamount* ((trade_profit)*5/2000)),eachamount)
              print(f"countlimit exceed  exit {position_type} at {exit_price} {current_time} with profit {trade_profit}  and total profit {net_profit} and each eamount is {eachamount}")
              triggered += 1
              position_type = None
              entry_price = None


              reversal_count = 0
              current_profit = 0
          countlimit=length
          continue



      if current_time_str == "15:15":

          if position_type:
              exit_price = hdfc_close_list[i]
              if position_type == 'BUY':
                  trade_profit = exit_price - entry_price
              else:
                  trade_profit = entry_price - exit_price
              if trade_profit >= 0:
                  total_profit += trade_profit
              else:
                  total_loss += abs(trade_profit)
              net_profit = total_profit - total_loss
              s=((trade_profit)*100*5/2000)
              l.append(s)
              eachamount += ( eachamount * (s / 100))-250
              demo_trade.append({  'symbol': 'HDFC','Date': entrydate,'Position_Type': position_type,'Time':current_time_str,'Exit_Price':exit_price})
              log_trade(1, entrydate, entrytime, current_time_str, position_type, entry_price, exit_price,( eachamount* ((trade_profit)*5/2000)),eachamount)
              print(f"3:15 PM exit {position_type} at {exit_price} {current_time} with profit {trade_profit}  and total profit {net_profit} and each eamount is {eachamount}")
              triggered += 1
              position_type = None
              entry_price = None
              reversal_count = 0
              current_profit = 0
          continue

      if position_type and not(-280 < df['priceDifference'][i] < 280):
              exit_price = hdfc_close_list[i]


              if position_type == 'BUY':
                  trade_profit = exit_price - entry_price
              else:
                  trade_profit = entry_price - exit_price
              if trade_profit >= 0:
                  total_profit += trade_profit
              else:
                  total_loss += abs(trade_profit)
              net_profit = total_profit - total_loss
              s=((trade_profit)*100*5/2000)
              l.append(s)
              eachamount +=( eachamount * (s / 100))-250
              demo_trade.append({  'symbol': 'HDFC','Date': entrydate,'Position_Type': position_type,'Time':current_time_str,'Exit_Price':exit_price})
              log_trade(1, entrydate, entrytime, current_time_str, position_type, entry_price, exit_price,( eachamount* ((trade_profit)*5/2000)),eachamount)
              print(f"maxcandle exit {position_type} at {exit_price} {current_time} with profit {trade_profit}  and total profit {net_profit} and each eamount is {eachamount}")
              triggered += 1
              position_type = None
              entry_price = None
              reversal_count = 0
              current_profit = 0
              continue




      if position_type == 'SELL' and (df['volMA_above_zero'][i]-df['volume'][i]<-420000) :
          print(hdf['priceDifference'][i])
          countlimit=24
          exit_price =hdfc_close_list[i]
          if position_type == 'BUY':
              trade_profit = exit_price - entry_price
          else:
              trade_profit = entry_price - exit_price

          if trade_profit >= 0:
              total_profit += trade_profit
              taken+=1
              s=((trade_profit)*5/2000)*100
              l.append(s)
              eachamount += ( eachamount * (s / 100))-250
              demo_trade.append({  'symbol': 'HDFC','Date': entrydate,'Position_Type': position_type,'Time':current_time_str,'Exit_Price':exit_price})
              log_trade(1, entrydate, entrytime, current_time_str, position_type, entry_price, exit_price,( eachamount* ((trade_profit)*5/2000)),eachamount)
              print(f"Reversed sell to buy at {exit_price} {current_time} with profit {trade_profit}  and total profit {net_profit} and each eamount is {eachamount}")
              entrydate=current_date_str
              entrytime=current_time_str
          else:
              total_loss += abs(trade_profit)
              s=((trade_profit)*100*5/2000)
              l.append(s)
              taken+=1
              eachamount +=( eachamount * (s / 100))-250
              log_trade(1, entrydate, entrytime, current_time_str, position_type, entry_price, exit_price,( eachamount* ((trade_profit)*5/2000)) ,eachamount)
              demo_trade.append({  'symbol': 'HDFC','Date': entrydate,'Position_Type': position_type,'Time':current_time_str,'Exit_Price':exit_price})
              print(f"Reversed sell to buy at {exit_price} {current_time} with loss {trade_profit }  and total profit {net_profit} and each eamount is {eachamount}")
              entrydate=current_date_str
              entrytime=current_time_str
          net_profit = total_profit - total_loss



          position_type = 'BUY'
          entry_price = exit_price
          demo_trade.append({  'symbol': 'HDFC','Date': entrydate,'Position_Type': position_type,'Time':current_time_str,'Entry_Price':entry_price})

          continue







      if triggered > 0:
          triggered = 0
          continue


      all_buy = (


          hdfc_close_list[i] > hdfc_close_list[i - 1] and
          icici_close_list[i] > icici_close_list[i - 1] and
          sbi_close_list[i] > sbi_close_list[i - 1]

      )


      all_sell = (


        hdfc_close_list[i] < hdfc_close_list[i - 1] and
          icici_close_list[i] < icici_close_list[i - 1] and
          sbi_close_list[i] < sbi_close_list[i - 1]

      )

      # x=hdfc_close_list[i-2]>hdfc_close_list[i-1] and abs(hdf['priceDifference'][i-1])>2.5*(abs(hdf['priceDifference'][i]))
      # y=hdfc_close_list[i-2]<hdfc_close_list[i-1] and abs(hdf['priceDifference'][i-1])>2.5*(abs(hdf['priceDifference'][i]))
      x=0
      y=0




      if all_buy and flag:


        if position_type == 'SELL'  :
            exit_price = hdfc_close_list[i]
            trade_profit = entry_price - exit_price
            if trade_profit >= 0:
                total_profit += trade_profit
            else:
                total_loss += abs(trade_profit)
            net_profit = total_profit - total_loss
            s=((trade_profit)*100/2000)
            l.append(s)
            eachamount +=( eachamount *5* (s / 100))-250
            log_trade(1, entrydate, entrytime, current_time_str, position_type, entry_price, exit_price,( eachamount* ((trade_profit)*5/2000)),eachamount)
            print(f"Exited sell at {exit_price} {current_time} with profit {trade_profit}  and total profit {net_profit} and each eamount is {eachamount}")
            position_type = None
            entry_price = None
            triggered += 1
        if  current_time_str != "15:00" and current_time_str != "13:30" and day_of_week!="Saturday" and current_time_str != "10:30" and current_time_str != "11:00" and position_type != 'buy'  and (df['volMA_above_zero'][i]-df['volume'][i]<1000000 or df['volMA_above_zero'][i]-df['volume'][i]>11000000) and -300 < df['priceDifference'][i] < 300 and not (-100 < df['priceDifference'][i] < 100) and not x :
            countlimit=14
            countCandles=0
            taken+=1
            entrydate=current_date_str
            entrytime=current_time_str
            print("difference price is ",df['volMA_above_zero'][i]-df['volume'][i])
            print(f"All confirm buy at {hdfc_close_list[i]} {current_time}")
            position_type = 'BUY'
            entry_price = hdfc_close_list[i]
            demo_trade.append({  'symbol': 'HDFC','Date': entrydate,'Position_Type': position_type,'Time':current_time_str,'Entry_Price':entry_price})
            reversal_count = 0
            current_profit = 0



      if all_sell and flag:
          # if position_type == 'buy':
          #     exit_price = hdfc_close_list[i]
          #     trade_profit = exit_price - entry_price
          #     if trade_profit >= 0:
          #         total_profit += trade_profit
          #     else:
          #         total_loss += abs(trade_profit)
          #     net_profit = total_profit - total_loss
          #     s=(int(trade_profit)*5*100/1800)
          #     l.append(s)
          #     eachamount += eachamount * (s / 100)
          #     print(f"Exited buy at {exit_price} {current_time} with profit {trade_profit} and total profit {net_profit} and each eamount is {eachamount}")
          #     position_type = None
          #     entry_price = None
          #     triggered += 1
          if  current_time_str != "15:00" and current_time_str != "13:30"  and day_of_week!="Saturday"  and position_type != 'sell' and (df['volMA_above_zero'][i]-df['volume'][i]<1000000  or df['volMA_above_zero'][i]-df['volume'][i]>11000000 ) and -300 < df['priceDifference'][i] < 300 and not (-50 < df['priceDifference'][i] < 50) and not y :
              countlimit=13
              countCandles=0
              print(current_time_str)
              taken+=1
              k= banknifty_open_list[i]
              print(f"All confirm sell at {hdfc_close_list[i]} {current_time}")
              entrydate=current_date_str
              entrytime=current_time_str
              store=df['volMA_above_zero'][i]-df['volume'][i]
              entry=banknifty_close_list[0]
              position_type = 'SELL'
              entry_price = hdfc_close_list[i]
              demo_trade.append({  'symbol': 'HDFC','Date': entrydate,'Position_Type': position_type,'Time':current_time_str,'Entry_Price':entry_price})
              reversal_count = 0
              current_profit = 0


      if (position_type == 'SELL' or position_type == 'BUY') and (reversal_count < max_reversals or countCandles < 13):
          flag=False
      else:
          flag=True
  amount=100000

  for percentage in l:
      amount += -250+( amount * (percentage / 100))


  profits = [row[7] for row in trade_data]
  # Parameters
  initial_capital = 100000
  leverage = 5
  trade_cost = 250
  stock_price = 2000 # Stock price
    # Absolute movement in stock price for each trade

  # Function to calculate compounded capital after each trade
  def calculate_compounded_profit(initial_capital, leverage, trade_cost, profits, stock_price):
      capital = initial_capital
      for profit_loss in profits:
          position_size = capital * leverage  # how much you can buy with leverage
          # Profit/Loss in Rupees
          profit_in_rupees = (profit_loss / stock_price) * position_size

          # Update capital
          capital += profit_in_rupees

          # Subtract trading cost
          # capital -= trade_cost

      return capital

  # Calculate final capital
  final_capital = calculate_compounded_profit(initial_capital, leverage, trade_cost, profits, stock_price)
  print(final_capital)

    # Example usage


  last_trade = demo_trade[-1]
  print(demo_trade)
  last_trade_time_str = last_trade.get('Time')  # e.g., "15:30"

  # Parse the time from the string (assuming it's in "HH:MM" 24-hour format)
  last_trade_time = datetime.strptime(last_trade_time_str, "%H:%M").time()

  # Get the current time
# Set the IST timezone
  india_timezone = pytz.timezone('Asia/Kolkata')

  # Get current time in IST
  current_time = datetime.now(india_timezone).time()
  print(current_time)

  # Convert both times to datetime objects (today's date)
  now = datetime.now(india_timezone).replace(second=0, microsecond=0)
  print(now)
  trade_time_today = now.replace(hour=last_trade_time.hour, minute=last_trade_time.minute)
  print(trade_time_today)

    # Check if the difference is less than 2 minutes
  if abs((now - trade_time_today).total_seconds()) < 902:
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

          Exit_send_to_firebase(last_trade)

  # print("demo-trade",demo_trade)
  print("Total profit: ", total_profit)
  print("Total loss: ", total_loss)
  print("Net profit: ", net_profit)
  print("Triggered: ", taken)
  print("amount : ",amount)
  betweenfrom= banknifty_datetime[0]
  between_strfrom = betweenfrom.strftime("%Y-%m-%d")
  betweento= banknifty_datetime[len(hdfc_close_list)-2]
  between_strto = betweento.strftime("%Y-%m-%d")
  print(between_strfrom, ' to ', between_strto)
  current_time = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")
  print("Current Time:", current_time)
  total_profit = sum(row[7] for row in trade_data)
  trade_data.append(["", "TOTAL", "", "", "", "", "", round(total_profit, 3),"",""])
  df = pd.DataFrame(trade_data, columns=["Serial No", "Date", "Entry Time", "Exit Time", "Position Type", "Entry Price", "Exit Price", "Profit",'profit/loss(100000)',"Amount(100000) After Charges"])
  csv_filename = "Hdfc_backtest_results.csv"
  df.to_csv(csv_filename, index=False)
  files.download(csv_filename)


def wait_for_next_15min_mark():
    global running
    while running:
        now = datetime.now()
        minutes_to_add = (15 - (now.minute % 15)) % 15
        if minutes_to_add == 0:
            minutes_to_add = 15

        next_mark = now.replace(second=0, microsecond=0) + timedelta(minutes=minutes_to_add)
        next_mark += timedelta(seconds=3)  # 3s buffer

        sleep_time = (next_mark - datetime.now()).total_seconds()
        if sleep_time > 0:
            print(f"⏳ Waiting {int(sleep_time)}s until {next_mark.strftime('%H:%M:%S')}")
            time.sleep(sleep_time)

        if running:  # check again before running
            my_function()

@app.route("/")
def home():
    return "Use /start to begin, /stop to end"

@app.route("/start")
def start():
    global running, thread
    if not running:
        running = True
        thread = threading.Thread(target=wait_for_next_15min_mark)
        thread.start()
        return "Trading loop started"
    return "Already running"

@app.route("/stop")
def stop():
    global running
    running = False
    return "Trading loop stopped"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
