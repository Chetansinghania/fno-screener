import streamlit as st
import pandas as pd
from fyers_apiv3 import fyersModel

st.title("LIVE F&O SCREENER")

client_id = "G5H4DU2N1A-100"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBfaWQiOiJHNUg0RFUyTjFBIiwidXVpZCI6Ijg2NDE5MTE2MzBmNDQ4ZDRhNWQyMjM2NmQ0NmQyMTQ1IiwiaXBBZGRyIjoiIiwibm9uY2UiOiIiLCJzY29wZSI6IiIsImRpc3BsYXlfbmFtZSI6IlhDMDgxNjEiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJmZmUzZGIzNjk1NmU5ZWU3ZThmOGVlMzA3MDE4NDVhMDYzMmZmOTIwMTNhNWI0ZWU4YTVjNzY4MiIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImF1ZCI6IltcImQ6MVwiLFwiZDoyXCIsXCJ4OjBcIixcIng6MVwiXSIsImV4cCI6MTc3OTk3NDM3NSwiaWF0IjoxNzc5OTQ0Mzc1LCJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJuYmYiOjE3Nzk5NDQzNzUsInN1YiI6ImF1dGhfY29kZSJ9.a1s4OHytK3r6Tvx3zziwbRTlgt79j7gLmpgy2snDynM"

fyers = fyersModel.FyersModel(
    client_id=client_id,
    token=token,
    is_async=False
)

stocks = [
    "NSE:RELIANCE-EQ",
    "NSE:HDFCBANK-EQ",
    "NSE:SBIN-EQ"
]

results = []

for stock in stocks:

    try:

        response = fyers.quotes({
            "symbols": stock
        })

        if response["s"] != "ok":
            raise Exception(response)

        stock_data = response["d"][0]["v"]

        results.append({
            "STOCK": stock,
            "PRICE": stock_data.get("lp")
        })

    except Exception as e:

        results.append({
            "STOCK": stock,
            "ERROR": str(e)
        })

df = pd.DataFrame(results)

st.dataframe(df)