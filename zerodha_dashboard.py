import streamlit as st
import pandas as pd
import requests
st.set_page_config(page_title="F&O Screener", layout="wide")
st.title("🚀 Live Institutional Momentum Screener")
client_id = "1N48IQB7GQ-100"
access_token = "'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCcUVzbmhHTXhoZlc2SzU1aXE0bXY1SUhKR2hUTlljNWl3MUw1UmIzWHprblpZbkpkSzlaTWlJalFzT29mTWtfNG40cm50S0lqWUxTckNpVExSOThtVkllcXloYWhtRGdpekozREhCT0xJN1Y0TlZ2ND0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI1ZjhjYTgwMDA0YmRlMThhN2NkMDNmZjY2ZGU4NDM5OTkzNGQ1MGI4MmE0MDJhZmI4MzU4NDYzMCIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEMwODE2MSIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzc5NjY5MDAwLCJpYXQiOjE3Nzk2MTYyMjUsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc3OTYxNjIyNSwic3ViIjoiYWNjZXNzX3Rva2VuIn0.kivfOJRPx0WPWjFvVao7LjA5ZSOAtDoheOCb6AKTYJc"
stocks = [
"NSE:RELIANCE-EQ",
"NSE:HDFCBANK-EQ",
"NSE:SBIN-EQ",
"NSE:TATAMOTORS-EQ",
"NSE:HAL-EQ",
"NSE:ADANIPORTS-EQ",
"NSE:BHEL-EQ"
]
headers = {
"Authorization": f"{client_id}:{access_token}"
}
results = []

for stock in stocks:

    try:

        url = f"https://api-t1.fyers.in/data/quotes?symbols={stock}"

        response = requests.get(
    url,
    headers={
        "Authorization": f"Bearer {access_token}"
    }
)

if "d" not in data:
    raise Exception(str(data))    

stock_data = data["d"][0]["v"]

        lp = stock_data.get("lp", 0)
        change_pct = stock_data.get("chp", 0)
        volume = stock_data.get("volume", 0)

        signal = "NO TRADE"

        if change_pct > 1:
            signal = "BUY"

        elif change_pct < -1:
            signal = "SELL"

        results.append({
            "STOCK": stock,
            "SIGNAL": signal,
            "PRICE": lp,
            "CHANGE %": change_pct,
            "VOLUME": volume
        })

    except Exception as e:

        results.append({
            "STOCK": stock,
            "ERROR": str(e)
        })

df = pd.DataFrame(results)
st.dataframe(df, width='stretch')

    