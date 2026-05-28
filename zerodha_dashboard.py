import streamlit as st
import pandas as pd
from fyers_apiv3 import fyersModel

st.set_page_config(page_title="F&O Screener", layout="wide")

st.title("📈 LIVE F&O SCREENER")

client_id = "G5H4DU2N1A-100"

with open("token.txt", "r") as f:
access_token = f.read().strip()

fyers = fyersModel.FyersModel(
client_id=client_id,
token=access_token,
is_async=False,
log_path=""
)

stocks = [
"NSE:RELIANCE-EQ",
"NSE:HDFCBANK-EQ",
"NSE:SBIN-EQ"
]

results = []

for stock in stocks:

```
try:

    response = fyers.quotes({
        "symbols": stock
    })

    if response.get("s") != "ok":
        results.append({
            "STOCK": stock,
            "ERROR": response.get("message")
        })
        continue

    values = response["d"][0]["v"]

    results.append({
        "STOCK": stock,
        "PRICE": values.get("lp"),
        "CHANGE %": values.get("chp"),
        "VOLUME": values.get("volume")
    })

except Exception as e:

    results.append({
        "STOCK": stock,
        "ERROR": str(e)
    })
```

df = pd.DataFrame(results)

st.dataframe(df, use_container_width=True)
