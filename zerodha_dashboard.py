:::writing{variant="standard" id="74281"}
import streamlit as st
import pandas as pd
import requests

st.title("LIVE F&O SCREENER")

access_token = "'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCcUVzbmhHTXhoZlc2SzU1aXE0bXY1SUhKR2hUTlljNWl3MUw1UmIzWHprblpZbkpkSzlaTWlJalFzT29mTWtfNG40cm50S0lqWUxTckNpVExSOThtVkllcXloYWhtRGdpekozREhCT0xJN1Y0TlZ2ND0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI1ZjhjYTgwMDA0YmRlMThhN2NkMDNmZjY2ZGU4NDM5OTkzNGQ1MGI4MmE0MDJhZmI4MzU4NDYzMCIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEMwODE2MSIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzc5NjY5MDAwLCJpYXQiOjE3Nzk2MTYyMjUsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc3OTYxNjIyNSwic3ViIjoiYWNjZXNzX3Rva2VuIn0.kivfOJRPx0WPWjFvVao7LjA5ZSOAtDoheOCb6AKTYJc"

stocks = [
    "NSE:RELIANCE-EQ",
    "NSE:HDFCBANK-EQ",
    "NSE:SBIN-EQ"
]

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

        data = response.json()

        if "d" not in data:
            raise Exception(str(data))

        stock_data = data["d"][0]["v"]

        lp = stock_data.get("lp", 0)

        results.append({
            "STOCK": stock,
            "PRICE": lp
        })

    except Exception as e:

        results.append({
            "STOCK": stock,
            "ERROR": str(e)
        })

df = pd.DataFrame(results)

st.dataframe(df)
:::