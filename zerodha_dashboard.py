import streamlit as st
import time
import requests
# ============================================
# FYERS CONFIG
# ============================================

client_id = "1N48IQB7GQ-100"

# PASTE ONLY ACCESS TOKEN BELOW
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCcUVzbmhHTXhoZlc2SzU1aXE0bXY1SUhKR2hUTlljNWl3MUw1UmIzWHprblpZbkpkSzlaTWlJalFzT29mTWtfNG40cm50S0lqWUxTckNpVExSOThtVkllcXloYWhtRGdpekozREhCT0xJN1Y0TlZ2ND0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI1ZjhjYTgwMDA0YmRlMThhN2NkMDNmZjY2ZGU4NDM5OTkzNGQ1MGI4MmE0MDJhZmI4MzU4NDYzMCIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEMwODE2MSIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzc5NjY5MDAwLCJpYXQiOjE3Nzk2MTYyMjUsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc3OTYxNjIyNSwic3ViIjoiYWNjZXNzX3Rva2VuIn0.kivfOJRPx0WPWjFvVao7LjA5ZSOAtDoheOCb6AKTYJc"

headers = {
    "Authorization": f"{client_id}:{access_token}"
}
symbol = "NSE:RELIANCE-EQ"
url = f"https://api-t1.fyers.in/data/quotes?symbols={symbol}"

response = requests.get(url, headers=headers)

data = response.json()
# ============================================
# ALL PREMIUM F&O STOCKS
# ============================================

stocks = [

    # ULTRA HIGH PRICE

    "NSE:MRF-EQ",
    "NSE:PAGEIND-EQ",
    "NSE:SHREECEM-EQ",
    "NSE:HONAUT-EQ",
    "NSE:3MINDIA-EQ",
    "NSE:BOSCHLTD-EQ",

    # INDUSTRIAL / CAPITAL GOODS

    "NSE:ABB-EQ",
    "NSE:POLYCAB-EQ",
    "NSE:SIEMENS-EQ",
    "NSE:CUMMINSIND-EQ",
    "NSE:HAVELLS-EQ",

    # AUTO

    "NSE:MARUTI-EQ",
    "NSE:EICHERMOT-EQ",
    "NSE:M&M-EQ",
    "NSE:BAJAJ-AUTO-EQ",

    # CEMENT / INFRA

    "NSE:ULTRACEMCO-EQ",
    "NSE:LT-EQ",

    # FINANCIALS

    "NSE:BAJFINANCE-EQ",
    "NSE:HDFCAMC-EQ",
    "NSE:MCX-EQ",
    "NSE:MUTHOOTFIN-EQ",

    # IT / TECH

    "NSE:COFORGE-EQ",
    "NSE:PERSISTENT-EQ",
    "NSE:LTIM-EQ",
    "NSE:MPHASIS-EQ",
    "NSE:OFSS-EQ",
    "NSE:NAUKRI-EQ",

    # FMCG / CONSUMER

    "NSE:TITAN-EQ",
    "NSE:NESTLEIND-EQ",
    "NSE:PIDILITIND-EQ",
    "NSE:BRITANNIA-EQ",

    # DEFENCE

    "NSE:HAL-EQ",

    # HEALTHCARE

    "NSE:APOLLOHOSP-EQ",
    "NSE:DIVISLAB-EQ",
    "NSE:TORNTPHARM-EQ",

    # SPECIAL MOMENTUM

    "NSE:TRENT-EQ",
    "NSE:INDIGO-EQ",
    "NSE:ICICIGI-EQ",
    "NSE:DIXON-EQ",
    "NSE:OBEROIRLTY-EQ",

    # LARGE CAPS

    "NSE:RELIANCE-EQ",
    "NSE:TCS-EQ",
    "NSE:HDFCBANK-EQ",
    "NSE:ICICIBANK-EQ",
    "NSE:INFY-EQ",
    "NSE:KOTAKBANK-EQ",

    # EXTRA HIGH BETA / F&O

    "NSE:ADANIENT-EQ",
    "NSE:ADANIPORTS-EQ",
    "NSE:TATAMOTORS-EQ",
    "NSE:SBIN-EQ",
    "NSE:AXISBANK-EQ",
    "NSE:INDUSINDBK-EQ",
    "NSE:TECHM-EQ",
    "NSE:HCLTECH-EQ",
    "NSE:TATASTEEL-EQ",
    "NSE:JSWSTEEL-EQ",
    "NSE:HINDALCO-EQ",
    "NSE:VEDL-EQ",
    "NSE:SAIL-EQ",
    "NSE:BEL-EQ",
    "NSE:BHEL-EQ",
    "NSE:DLF-EQ",
    "NSE:IRCTC-EQ",
    "NSE:PVRINOX-EQ"

]

# ============================================
# PAGE SETTINGS
# ============================================

st.set_page_config(
    page_title="Professional FnO Momentum Screener",
    layout="wide"
)

st.title("📊 PROFESSIONAL F&O MOMENTUM SCREENER")

st.write("Institutional Intraday Trading Dashboard")

refresh_time = st.slider(
    "Refresh Time (seconds)",
    2,
    30,
    5
)

start_scan = st.button("🚀 START LIVE SCAN")

# ============================================
# MARKET SCANNER
# ============================================

def scan_market():

    results = []

    for stock in stocks:

        try:

            response = fyers.quotes({
                "symbols": stock
            })

            if response.get("s") != "ok":
                continue

            data = response["d"][0]["v"]

            lp = data.get("lp")
            open_price = data.get("open_price")
            volume = data.get("volume", 0)
            atp = data.get("atp")
            high_price = data.get("high_price")
            low_price = data.get("low_price")

            if not lp or not open_price:
                continue

            # ============================================
            # FILTER STOCK PRICE > 2500
            # ============================================

            if lp < 2500:
                continue

            # ============================================
            # PRICE CHANGE %
            # ============================================

            change = ((lp - open_price) / open_price) * 100

            # ============================================
            # ATR %
            # ============================================

            atr = 0

            if high_price and low_price:
                atr = ((high_price - low_price) / lp) * 100

            # ============================================
            # SCORE ENGINE
            # ============================================

            score = 0

            # MOMENTUM

            if change > 0.7:
                score += 2

            elif change < -0.7:
                score -= 2

            # VWAP FILTER

            if atp:

                if lp > atp:
                    score += 2

                else:
                    score -= 1

            # VOLUME FILTER

            if volume > 500000:
                score += 2

            # ATR FILTER

            if atr > 1.2:
                score += 2

            # ============================================
            # SIGNAL ENGINE
            # ============================================

            if score >= 6:
                signal = "🟢 STRONG BUY"

            elif score >= 4:
                signal = "🟢 BUY"

            elif score <= -6:
                signal = "🔴 STRONG SELL"

            elif score <= -4:
                signal = "🔴 SELL"

            else:
                signal = "⚪ NO TRADE"

            # ============================================
            # ENTRY / STOPLOSS / TARGET
            # ============================================

            entry = round(lp, 2)

            if "BUY" in signal:

                sl = round(lp * 0.995, 2)
                target = round(lp * 1.01, 2)

            elif "SELL" in signal:

                sl = round(lp * 1.005, 2)
                target = round(lp * 0.99, 2)

            else:

                sl = "-"
                target = "-"

            # ============================================
            # OPTION STRIKE
            # ============================================

            atm = round(lp / 50) * 50

            # ============================================
            # SAVE RESULT
            # ============================================

            results.append({

                "STOCK": stock,
                "PRICE": round(lp, 2),
                "% CHANGE": round(change, 2),
                "ATR %": round(atr, 2),
                "VOLUME": volume,
                "SCORE": score,
                "SIGNAL": signal,
                "ENTRY": entry,
                "STOP LOSS": sl,
                "TARGET": target,
                "ATM OPTION": atm

            })

        except Exception as e:

            results.append({

                "STOCK": stock,
                "ERROR": str(e)

            })

    # ============================================
    # RANK STRONGEST STOCKS
    # ============================================

    results = sorted(
        results,
        key=lambda x: x.get("SCORE", 0),
        reverse=True
    )

    return results

# ============================================
# LIVE DASHBOARD
# ============================================

if start_scan:

    placeholder = st.empty()

    while True:

        market_data = scan_market()

        with placeholder.container():

            st.subheader("📡 LIVE MARKET SCAN")

            st.dataframe(
                market_data,
                use_container_width=True
            )

        time.sleep(refresh_time)
