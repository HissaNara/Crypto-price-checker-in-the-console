from flask import Flask
import requests
import time
import threading

app=Flask(__name__)

def price_loop():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    while True:
        data=requests.get(url).json()
        price=data["price"]
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        print(now,":",price)
        time.sleep(1)

@app.route("/")
def index():
    return "Online!"

if __name__ == "__main__":
    t = threading.Thread(target=price_loop, daemon=True)
    t.start() 

    app.run(debug=False)