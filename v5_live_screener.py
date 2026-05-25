from fyers_apiv3 import fyersModel

# =========================
# FYERS LOGIN
# =========================

client_id = "YOUR_APP_ID"
access_token = "YOUR_ACCESS_TOKEN"

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
# SCANNER (LIVE MOMENTUM)
# =========================

def run_scanner():

    print("\n====================")
    print("LIVE INTRADAY SCREENER")
    print("====================\n")

    for stock in stocks:

        data = {
            "symbols": stock
        }

        response = fyers.quotes(data)

        if 'd' not in response:
            print(stock, "NO DATA")
            continue

        try:
            lp = response['d'][0]['v']['lp']
            open_price = response['d'][0]['v']['open_price']

            change = ((lp - open_price) / open_price) * 100

            # SIMPLE INTRADAY LOGIC
            if change > 0.5:
                print(stock, "👉 BUY WATCH |", round(change, 2), "%")

            elif change < -0.5:
                print(stock, "👉 SELL WATCH |", round(change, 2), "%")

            else:
                print(stock, "👉 NO TRADE |", round(change, 2), "%")

        except:
            print(stock, "DATA ERROR")


# =========================
# RUN ONCE
# =========================

run_scanner()