from fyers_apiv3 import fyersModel

# =========================
# AUTH
# =========================

client_id = "1N48IQB7GQ-100"
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCcUVzbmhHTXhoZlc2SzU1aXE0bXY1SUhKR2hUTlljNWl3MUw1UmIzWHprblpZbkpkSzlaTWlJalFzT29mTWtfNG40cm50S0lqWUxTckNpVExSOThtVkllcXloYWhtRGdpekozREhCT0xJN1Y0TlZ2ND0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI1ZjhjYTgwMDA0YmRlMThhN2NkMDNmZjY2ZGU4NDM5OTkzNGQ1MGI4MmE0MDJhZmI4MzU4NDYzMCIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEMwODE2MSIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzc5NjY5MDAwLCJpYXQiOjE3Nzk2MTYyMjUsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc3OTYxNjIyNSwic3ViIjoiYWNjZXNzX3Rva2VuIn0.kivfOJRPx0WPWjFvVao7LjA5ZSOAtDoheOCb6AKTYJc "

fyers = fyersModel.FyersModel(
    client_id=client_id,
    token=access_token
)

# =========================
# CONFIG
# =========================

TIMEFRAME = "5m"   # BEST: 5m for entry | 15m for confirmation

stocks = [
    "NSE:RELIANCE-EQ",
    "NSE:HDFCBANK-EQ",
    "NSE:SBIN-EQ",
    "NSE:TATAMOTORS-EQ",
    "NSE:ADANIPORTS-EQ",
    "NSE:HAL-EQ",
    "NSE:BHEL-EQ"
]

# =========================
# NIFTY FILTER
# =========================

def get_nifty():
    res = fyers.quotes({"symbols": "NSE:NIFTY50-INDEX"})
    if res.get("s") != "ok":
        return 0
    return res["d"][0]["v"].get("lp", 0)

nifty_price = get_nifty()

# =========================
# HELPERS
# =========================

def volume_explosion(v):
    vol = v.get("volume", 0)
    avg = v.get("atp", vol)  # proxy for avg volume
    return vol > (avg * 2)

def atr_percent(v):
    high = v.get("high_price")
    low = v.get("low_price")
    close = v.get("lp")
    if not high or not low or not close:
        return 0
    return ((high - low) / close) * 100

def vwap(v):
    return v.get("atp", v.get("lp"))

def option_chain(price):
    atm = round(price / 50) * 50
    return {
        "ATM": atm,
        "CALL_ITM": atm - 50,
        "PUT_ITM": atm + 50,
        "CALL_OTM": atm + 100,
        "PUT_OTM": atm - 100
    }

def sector_strength(score):
    if score > 6:
        return "STRONG BULLISH SECTOR"
    elif score < -6:
        return "STRONG BEARISH SECTOR"
    return "NEUTRAL"

# =========================
# SCREENER ENGINE
# =========================

print("\n====================")
print("FINAL INSTITUTIONAL FYERS SCREENER V3")
print("====================\n")

results = []

for stock in stocks:

    try:
        res = fyers.quotes({"symbols": stock})

        if res.get("s") != "ok":
            continue

        v = res["d"][0]["v"]

        lp = v.get("lp")
        open_price = v.get("open_price")
        volume = v.get("volume", 0)

        if not lp or not open_price:
            continue

        score = 0

        # =========================
        # MOMENTUM
        # =========================

        change = ((lp - open_price) / open_price) * 100

        if change > 0.7:
            score += 3
        elif change < -0.7:
            score -= 3

        # =========================
        # VWAP FILTER
        # =========================

        vw = vwap(v)
        if vw:
            if lp > vw:
                score += 2
            else:
                score -= 2

        # =========================
        # VOLUME CONFIRMATION
        # =========================

        if volume_explosion(v):
            score += 3

        # =========================
        # ATR FILTER
        # =========================

        atr = atr_percent(v)

        if atr > 1.2:
            score += 2
        else:
            score -= 1

        # =========================
        # RELATIVE STRENGTH
        # =========================

        nifty_change = 0
        if nifty_price:
            nifty_change = 0.3  # simplified baseline

        rs = change - nifty_change

        if rs > 1:
            score += 3
        elif rs < -1:
            score -= 2

        # =========================
        # BREAKOUT LOGIC
        # =========================

        high = v.get("high_price")
        low = v.get("low_price")

        if high and lp > high * 0.995:
            score += 2

        if low and lp < low * 1.005:
            score -= 2

        # =========================
        # FINAL DECISION
        # =========================

        if score >= 7:
            signal = "STRONG BUY"
        elif score >= 4:
            signal = "BUY"
        elif score <= -7:
            signal = "STRONG SELL"
        elif score <= -4:
            signal = "SELL"
        else:
            signal = "NO TRADE"

        results.append({
            "stock": stock,
            "score": score,
            "signal": signal,
            "price": lp,
            "change": change,
            "atr": atr,
            "volume": volume,
            "options": option_chain(lp)
        })

    except:
        continue

# =========================
# RANKING
# =========================

results.sort(key=lambda x: x["score"], reverse=True)

print("NIFTY PRICE:", nifty_price)
print("\nTOP MOMENTUM STOCKS:\n")

for r in results:

    print("--------------------")
    print(r["stock"])
    print("SIGNAL:", r["signal"])
    print("SCORE:", r["score"])
    print("PRICE:", r["price"])
    print("CHANGE %:", round(r["change"], 2))
    print("ATR %:", round(r["atr"], 2))
    print("VOLUME:", r["volume"])
    print("OPTIONS:", r["options"])

    # =========================
    # TRADE PLAN
    # =========================

    if r["signal"] in ["BUY", "STRONG BUY"]:

        entry = r["price"]
        sl = entry * 0.995
        target = entry * 1.01

        print("ENTRY:", round(entry, 2))
        print("STOP LOSS:", round(sl, 2))
        print("TARGET:", round(target, 2))

    elif r["signal"] in ["SELL", "STRONG SELL"]:

        entry = r["price"]
        sl = entry * 1.005
        target = entry * 0.99

        print("ENTRY:", round(entry, 2))
        print("STOP LOSS:", round(sl, 2))
        print("TARGET:", round(target, 2))
