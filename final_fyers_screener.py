from fyers_apiv3 import fyersModel

# =========================
# LOGIN (EDIT ONLY THIS)
# =========================

client_id = "1N48IQB7GQ-100"
access_token = "1N48IQB7GQ-100:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBfaWQiOiIxTjQ4SVFCN0dRIiwidXVpZCI6ImY2MWM3NTIwMTVjZTQ4OWM5ZjA3MTYxYjFjOTI3NWIxIiwiaXBBZGRyIjoiIiwibm9uY2UiOiIiLCJzY29wZSI6IiIsImRpc3BsYXlfbmFtZSI6IlhDMDgxNjEiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI2ODY1NDFhZjVmZDliOWIyNWI0YmJlZTcyZTE3NmVhOGExOWExNjQ4NWJlYmVkMmMzZGZlNzFmMSIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImF1ZCI6IltcImQ6MVwiLFwiZDoyXCIsXCJ4OjBcIixcIng6MVwiLFwieDoyXCJdIiwiZXhwIjoxNzc5NjQzMTEzLCJpYXQiOjE3Nzk2MTMxMTMsImlzcyI6ImFwaS5sb2dpbi5meWVycy5pbiIsIm5iZiI6MTc3OTYxMzExMywic3ViIjoiYXV0aF9jb2RlIn0.LFemJx6IB2wWF-JwCVRz7DvJKPm6-GLOAXrk9vt3GGk"

fyers = fyersModel.FyersModel(
    client_id=client_id,
    token=access_token
)

# =========================
# STOCK LIST
# =========================

stocks = [
    "NSE:RELIANCE-EQ",
    "NSE:HDFCBANK-EQ",
    "NSE:SBIN-EQ",
    "NSE:TATAMOTORS-EQ",
    "NSE:ADANIPORTS-EQ",
    "NSE:HAL-EQ",
    "NSE:BHEL-EQ"
]

# =========================
# SCREENER LOGIC
# =========================

def run_scanner():

    print("\n====================")
    print("FINAL FYERS INTRADAY SCREENER")
    print("====================\n")

    for stock in stocks:

        try:
            response = fyers.quotes({"symbols": "NSE:RELIANCE-EQ"})
            print(response)

            # debug safety
            if response.get("s") != "ok":
                print(stock, "NO DATA")
                continue

            item = response["d"][0]

            lp = item["v"]["lp"]
            open_price = item["v"]["open_price"]

            change = ((lp - open_price) / open_price) * 100

            if change > 0.5:
                print(stock, "👉 BUY", round(change, 2), "%")

            elif change < -0.5:
                print(stock, "👉 SELL", round(change, 2), "%")

            else:
                print(stock, "👉 NO TRADE", round(change, 2), "%")

        except Exception as e:
            print(stock, "ERROR", str(e))


# =========================
# RUN
# =========================

run_scanner()
