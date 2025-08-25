Skip to content
Navigation Menu
HissaNara
Crypto-price-checker-in-the-console

Type / to search
Code
Issues
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
Comparing changes
Choose two branches to see what’s changed or to start a new pull request. If you need to, you can also  or learn more about diff comparisons.
 
...
 
 1 commit
 1 file changed
 1 contributor
Commits on Aug 25, 2025
Update app.py

@HissaNara
HissaNara authored 15 minutes ago
 Showing  with 11 additions and 24 deletions.
 35 changes: 11 additions & 24 deletions35  
app.py
Original file line number	Diff line number	Diff line change
@@ -1,35 +1,22 @@
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
Footer
© 2025 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact
Manage cookies
Do not share my personal information
Comparing 073289aec75f990cdf67f89b03dfc272aa43a834...9a93fd5c553e3d0763fb769c2851fce89a59a024 · HissaNara/Crypto-price-checker-in-the-console
