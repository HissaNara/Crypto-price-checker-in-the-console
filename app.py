from flask import Flask, jsonify, render_template
import requests, time

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/price")
def get_price():
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        url = "https://api.binance.com/api/v3/ticker/price"
        data = requests.get(url, params={"symbol": "BTCUSDT"}, timeout=5).json()
        price = data["price"]
    except Exception as e:
        price = None
    return jsonify({"now": now, "price": price})

if __name__ == "__main__":
    app.run(debug=False)
