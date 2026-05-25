from fyers_apiv3 import fyersModel
import pandas as pd
import ta

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
    "NSE:HAL-EQ",
    "NSE:BHEL-EQ",
    "NSE:ADANIPORTS-EQ",
    "NSE:SBIN-EQ"
]

# =========================
# SCANNER LOOP
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
    # VWAP
    # =========================

    df['vwap'] = ta.volume.volume_weighted_average_price(
        high=df['high'],
        low=df['low'],
        close=df['close'],
        volume=df['volume']
    )

    # =========================
    # SMA 20
    # =========================

    df['sma20'] = ta.trend.sma_indicator(
        df['close'],
        window=20
    )

    # =========================
    # ATR
    # =========================

    df['atr'] = ta.volatility.average_true_range(
        high=df['high'],
        low=df['low'],
        close=df['close'],
        window=14
    )

    # =========================
    # LATEST VALUES
    # =========================

    close_price = df['close'].iloc[-1]

    vwap = df['vwap'].iloc[-1]

    sma20 = df['sma20'].iloc[-1]

    atr = df['atr'].iloc[-1]

    volume = df['volume'].iloc[-1]

    avg_volume = df['volume'].rolling(20).mean().iloc[-1]

    # =========================
    # BUY LOGIC
    # =========================

    if (
        close_price > vwap
        and close_price > sma20
        and volume > avg_volume * 2
        and atr > 5
    ):

        print(stock, "--> STRONG BUY")

    # =========================
    # SELL LOGIC
    # =========================

    elif (
        close_price < vwap
        and close_price < sma20
        and volume > avg_volume * 2
    ):

        print(stock, "--> STRONG SELL")

    else:

        print(stock, "--> NO TRADE")
