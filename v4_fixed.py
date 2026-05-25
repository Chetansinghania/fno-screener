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
    "NSE:SBIN-EQ",
    "NSE:HDFCBANK-EQ",
    "NSE:TATAMOTORS-EQ"
]

# =========================
# SAFE NIFTY TREND
# =========================

def nifty_trend():

    try:
        data = {"symbols": "NSE:NIFTY50-INDEX"}

        response = fyers.quotes(data)

        if 'd' not in response:
            return "BULLISH"

        lp = response['d'][0]['v'].get('lp', 0)
        open_price = response['d'][0]['v'].get('open_price', 0)

        if lp > open_price:
            return "BULLISH"
        else:
            return "BEARISH"

    except:
        return "BULLISH"


# =========================
# SCANNER
# =========================

def run_scanner():

    market_trend = nifty_trend()

    print("\n====================")
    print("NIFTY =", market_trend)
    print("====================\n")

    for stock in stocks:

        score = 0

        data = {
            "symbol": stock.replace("NSE:", ""),
            "resolution": "5",
            "date_format": "1",
            "range_from": "2025-11-0",
            "range_to": "2025-11-30",
            "cont_flag": "1"
        }
        print("REQUEST:", stock)
        response = fyers.history(data)

        if 'candles' not in response:
            print(stock, "--> NO DATA")
            continue

        candles = response['candles']

        df = pd.DataFrame(candles, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume'
        ])

        # Indicators
        df['sma20'] = ta.trend.sma_indicator(df['close'], window=20)

        df['vwap'] = ta.volume.volume_weighted_average_price(
            high=df['high'],
            low=df['low'],
            close=df['close'],
            volume=df['volume']
        )

        bb = ta.volatility.BollingerBands(df['close'], window=20, window_dev=2)
        df['bb_mid'] = bb.bollinger_mavg()

        df['atr'] = ta.volatility.average_true_range(
            df['high'], df['low'], df['close'], window=14
        )

        # Latest values
        close_price = df['close'].iloc[-1]
        latest_open = df['open'].iloc[-1]
        previous_close = df['close'].iloc[-2]
        previous_open = df['open'].iloc[-2]

        candle_body = abs(close_price - latest_open)

        vwap = df['vwap'].iloc[-1]
        sma20 = df['sma20'].iloc[-1]
        bb_mid = df['bb_mid'].iloc[-1]
        atr = df['atr'].iloc[-1]

        volume = df['volume'].iloc[-1]
        avg_volume = df['volume'].rolling(20).mean().iloc[-1]

        # Relative strength (simple)
        stock_change = (close_price - latest_open) / latest_open * 100

        nifty_data = {"symbols": "NSE:NIFTY50-INDEX"}
        nifty_response = fyers.quotes(nifty_data)

        try:
            nifty_lp = nifty_response['d'][0]['v'].get('lp', 0)
            nifty_open = nifty_response['d'][0]['v'].get('open_price', 0)
            nifty_change = (nifty_lp - nifty_open) / nifty_open * 100
        except:
            nifty_change = 0

        # Scoring system
        if close_price > vwap:
            score += 2

        if close_price > sma20:
            score += 2

        if close_price > bb_mid:
            score += 1

        if volume > avg_volume * 1.5:
            score += 3

        if close_price > latest_open:
            score += 2

        if stock_change > nifty_change:
            score += 3

        if close_price > previous_close:
            score += 2

        if candle_body > atr * 0.3:
            score += 2

        if previous_close > previous_open:
            score += 1

        # Final output
        if market_trend == "BULLISH":

            if score >= 12:
                print(stock, "--> STRONG BUY | SCORE =", score)

            elif score >= 8:
                print(stock, "--> WATCHLIST | SCORE =", score)

            else:
                print(stock, "--> NO TRADE | SCORE =", score)

        else:

            if score <= 4:
                print(stock, "--> STRONG SELL")
            else:
                print(stock, "--> NO TRADE | SCORE =", score)


run_scanner()
