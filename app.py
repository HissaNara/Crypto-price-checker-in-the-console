from flask import Flask, jsonify, render_template
import requests, time, threading

app = Flask(__name__)

latest_time = ""
latest_price = ""

def price_loop():
    global latest_time, latest_price
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    while True:
        try:
            data = requests.get(url, timeout=5).json()
            latest_price = data["price"]
            latest_time = time.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            latest_price = None
            latest_time = time.strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(1) 

t = threading.Thread(target=price_loop, daemon=True)
t.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/price")
def get_price():
    return jsonify({"now": latest_time, "price": latest_price})

if __name__ == "__main__":
    app.run(debug=False)
