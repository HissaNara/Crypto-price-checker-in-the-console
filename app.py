from flask import Flask,jsonify,render_template_string
import requests
import time
import threading

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

@app.route("/")
def index():
    return render_template_string("""
        <h1>BTC/USDT 価格</h1>
        <p id="output">Loading...</p>

        <script>
        async function fetchPrice() {
            let res = await fetch("/price");
            let data = await res.json();
            document.getElementById("output").innerText =
                data.now + " : " + data.price;
        }
        setInterval(fetchPrice, 1000);  // 1秒ごとに最新値で上書き
        fetchPrice(); // 最初に1回呼び出す
        </script>
    """)

@app.route("/price")
def price():
    return jsonify({"now": latest_time, "price": latest_price})

if __name__ == "__main__":
    t = threading.Thread(target=price_loop, daemon=True)
    t.start() 

    app.run(debug=False)
