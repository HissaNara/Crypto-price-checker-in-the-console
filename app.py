from flask import Flask,jsonify,render_template
import requests
import time
import threading
from flask import Flask, jsonify, render_template
import requests, time

latest_time = ""
latest_price = ""

app=Flask(__name__)

def price_loop():
    global latest_time, latest_price
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    while True:
        data=requests.get(url).json()
        price=data["price"]
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        print(now,":",price)
        latest_time = now
        latest_price = price
        time.sleep(1)
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/price")
def get_price():
    return jsonify({"now": latest_time, "price": latest_price})
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        url = "https://api.binance.com/api/v3/ticker/price"
        data = requests.get(url, params={"symbol": "BTCUSDT"}, timeout=5).json()
        price = data["price"]
    except Exception as e:
        price = None
    return jsonify({"now": now, "price": price})

if __name__ == "__main__":
    t = threading.Thread(target=price_loop, daemon=True)
    t.start() 

    app.run(debug=False)
