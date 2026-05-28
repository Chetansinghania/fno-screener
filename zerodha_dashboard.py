import streamlit as st
import pandas as pd
import requests

st.title("LIVE F&O SCREENER")

access_token = "G5H4DU2N1A-100:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBfaWQiOiJHNUg0RFUyTjFBIiwidXVpZCI6ImU1NjlkNTQxZDc1ZDRlOTdiMjMyZmU1ZDY1YTUzYmUwIiwiaXBBZGRyIjoiIiwibm9uY2UiOiIiLCJzY29wZSI6IiIsImRpc3BsYXlfbmFtZSI6IlhDMDgxNjEiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJmZmUzZGIzNjk1NmU5ZWU3ZThmOGVlMzA3MDE4NDVhMDYzMmZmOTIwMTNhNWI0ZWU4YTVjNzY4MiIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImF1ZCI6IltcImQ6MVwiLFwiZDoyXCIsXCJ4OjBcIixcIng6MVwiXSIsImV4cCI6MTc3OTk3MjEyNCwiaWF0IjoxNzc5OTQyMTI0LCJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJuYmYiOjE3Nzk5NDIxMjQsInN1YiI6ImF1dGhfY29kZSJ9.lDj_85JhFAW4QCYNOVGSYpI9lbEUacJKv6zX-AJfptE"

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