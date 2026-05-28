import streamlit as st
import pandas as pd
from fyers_apiv3 import fyersModel

st.title("LIVE F&O SCREENER")

client_id = "G5H4DU2N1A-100"

with open("token.txt") as f:
access_token = f.read().strip()

fyers = fyersModel.FyersModel(
client_id=client_id,
token=access_token
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

    results.append({
        "STOCK": stock,
        "DATA": response
    })

except Exception as e:

    results.append({
        "STOCK": stock,
        "ERROR": str(e)
    })
```

df = pd.DataFrame(results)

st.dataframe(df)
