from fyers_apiv3 import fyersModel
import pandas as pd

# =========================
# FYERS LOGIN
# =========================

client_id = "1N48IQB7GQ-100"

access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCcUVkbkFTRThFS2N2MjdBWXFwSXlnVUpPNG1XQXB4N1dhOEd6NjhXREd6U1ExYUg4YkhMNDl4R0k1dDN2TmJrNlk3TTNGeVVKanRIUC1MVzVWV00xbkxYNlBqWWl6cG9ZT045MElySnZrbVJfaTRfVT0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI2ODY1NDFhZjVmZDliOWIyNWI0YmJlZTcyZTE3NmVhOGExOWExNjQ4NWJlYmVkMmMzZGZlNzFmMSIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEMwODE2MSIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzc5NTgyNjAwLCJpYXQiOjE3Nzk1NTQ3NTIsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc3OTU1NDc1Miwic3ViIjoiYWNjZXNzX3Rva2VuIn0.41wM1RgcBif_sqmUDgBwtFSpXprL2UqGAY_OkNTxrCQ"

fyers = fyersModel.FyersModel(
    client_id=client_id,
    token=access_token
)

# =========================
# STOCK LIST
# =========================

stocks = [
    "NSE:RELIANCE-EQ",
    "NSE:TATAMOTORS-EQ",
    "NSE:HAL-EQ",
    "NSE:BHEL-EQ",
    "NSE:ADANIPORTS-EQ"
]

# =========================
# SCANNER
# =========================

for stock in stocks:

    data = {
        "symbol": stock,
        "resolution": "5",
        "date_format": "1",
        "range_from": "2026-05-20",
        "range_to": "2026-05-23",
        "cont_flag": "1"
    }

    response = fyers.history(data)

    if 'candles' not in response:
        print(stock, "--> DATA NOT AVAILABLE")
        continue

    candles = response['candles']

    df = pd.DataFrame(
        candles,
        columns=[
            'timestamp',
            'open',
            'high',
            'low',
            'close',
            'volume'
        ]
    )

    # =========================
    # PREVIOUS DAY HIGH
    # =========================

    previous_day_high = df['high'].iloc[-20]

    # =========================
    # FIRST 5-MIN CLOSE
    # =========================

    first_5min_close = df['close'].iloc[-1]

    # =========================
    # SMA 20
    # =========================

    sma20 = df['close'].rolling(20).mean().iloc[-1]

    # =========================
    # BUY SIGNAL
    # =========================

    if (
        first_5min_close > previous_day_high
        and first_5min_close > sma20
        and first_5min_close < sma20 * 1.01
    ):

        print(stock, "--> BUY SIGNAL")

    # =========================
    # SELL SIGNAL
    # =========================

    elif (
        first_5min_close < previous_day_high
        and first_5min_close < sma20
    ):

        print(stock, "--> SELL SIGNAL")

    else:

        print(stock, "--> NO TRADE")
