from flask import Flask, jsonify, render_template
import requests, time, threading

app = Flask(__name__)

BINANCE_URL = "https://api.binance.com/api/v3/ticker/price"
SYMBOL = "BTCUSDT"

latest_time = ""
latest_price = ""

def fetch_once():
    """Binanceから一度だけ取得して (now, price) を返す"""
    r = requests.get(BINANCE_URL, params={"symbol": SYMBOL}, timeout=5)
    r.raise_for_status()
    data = r.json()
    return time.strftime("%Y-%m-%d %H:%M:%S"), data["price"]

def price_loop():
    """一定間隔で取得してキャッシュを更新"""
    global latest_time, latest_price
    while True:
        try:
            now, price = fetch_once()
            latest_time, latest_price = now, price
        except Exception:
            # 失敗時は前回値を保持（必要ならログ出力）
            pass
        time.sleep(10)  # ★ ここで間隔調整（5〜10秒推奨）

# ★ gunicorn/Render でも必ず起動するよう、読み込み時にスレッド開始
t = threading.Thread(target=price_loop, daemon=True)
t.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/price")
def get_price():
    """キャッシュを返す。初回未取得ならフォールバックで1回だけ同期取得"""
    global latest_time, latest_price
    if not latest_price:
        try:
            now, price = fetch_once()
            latest_time, latest_price = now, price
        except Exception:
            # 初回取得も失敗した場合は空のまま返す（HTTP 503で伝える）
            return jsonify({"now": latest_time, "price": latest_price}), 503
    return jsonify({"now": latest_time, "price": latest_price})

if __name__ == "__main__":
    app.run(debug=False)
