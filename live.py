from fyers_apiv3 import fyersModel

# =========================
# FYERS DETAILS
# =========================

client_id = "1N48IQB7GQ-100"

access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCcUVkbkFTRThFS2N2MjdBWXFwSXlnVUpPNG1XQXB4N1dhOEd6NjhXREd6U1ExYUg4YkhMNDl4R0k1dDN2TmJrNlk3TTNGeVVKanRIUC1MVzVWV00xbkxYNlBqWWl6cG9ZT045MElySnZrbVJfaTRfVT0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI2ODY1NDFhZjVmZDliOWIyNWI0YmJlZTcyZTE3NmVhOGExOWExNjQ4NWJlYmVkMmMzZGZlNzFmMSIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEMwODE2MSIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzc5NTgyNjAwLCJpYXQiOjE3Nzk1NTQ3NTIsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc3OTU1NDc1Miwic3ViIjoiYWNjZXNzX3Rva2VuIn0.41wM1RgcBif_sqmUDgBwtFSpXprL2UqGAY_OkNTxrCQ"

# =========================
# CONNECT FYERS
# =========================

fyers = fyersModel.FyersModel(
    client_id=client_id,
    token=access_token
)

# =========================
# LIVE MARKET DATA
# =========================

data = {
    "symbols":"NSE:RELIANCE-EQ"
}

response = fyers.quotes(data)

print(response)
