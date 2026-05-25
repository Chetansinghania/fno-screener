from fyers_apiv3 import fyersModel

client_id = "1N48IQB7GQ-100"

access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCcUVzbmhHTXhoZlc2SzU1aXE0bXY1SUhKR2hUTlljNWl3MUw1UmIzWHprblpZbkpkSzlaTWlJalFzT29mTWtfNG40cm50S0lqWUxTckNpVExSOThtVkllcXloYWhtRGdpekozREhCT0xJN1Y0TlZ2ND0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI1ZjhjYTgwMDA0YmRlMThhN2NkMDNmZjY2ZGU4NDM5OTkzNGQ1MGI4MmE0MDJhZmI4MzU4NDYzMCIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEMwODE2MSIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzc5NjY5MDAwLCJpYXQiOjE3Nzk2MTYyMjUsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc3OTYxNjIyNSwic3ViIjoiYWNjZXNzX3Rva2VuIn0.kivfOJRPx0WPWjFvVao7LjA5ZSOAtDoheOCb6AKTYJc"

fyers = fyersModel.FyersModel(
    client_id=client_id,
    token=access_token
)
# =========================
# FYERS INIT (CORRECT METHOD)
# =========================

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
# TEST & SCANNER
# =========================

print("\n====================")
print("FINAL FYERS SCREENER (FIXED)")
print("====================\n")

# 🔵 STEP 1: TEST CONNECTION FIRST
test = fyers.quotes({"symbols": "NSE:SBIN-EQ"})
print("TEST RESPONSE:", test)

if test.get("s") != "ok":
    print("\n❌ TOKEN ERROR OR API ISSUE")
    print("👉 Fix: regenerate access token correctly")
    exit()

# 🔵 STEP 2: SCAN ALL STOCKS
for stock in stocks:

    try:
        response = fyers.quotes({"symbols": stock})

        if response.get("s") != "ok":
            print(stock, "NO DATA")
            continue

        data = response["d"][0]["v"]

        lp = data["lp"]
        open_price = data["open_price"]

        change = ((lp - open_price) / open_price) * 100

        if change > 0.5:
            print(stock, "👉 BUY", round(change, 2), "%")

        elif change < -0.5:
            print(stock, "👉 SELL", round(change, 2), "%")

        else:
            print(stock, "👉 NO TRADE", round(change, 2), "%")

    except Exception as e:
        print(stock, "ERROR:", str(e))
