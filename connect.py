from fyers_apiv3 import fyersModel
import webbrowser

APP_ID = "1N48IQB7GQ-100"
SECRET_KEY = "7TX0ILW68X"

REDIRECT_URI = "https://127.0.0.1"

session = fyersModel.SessionModel(
    client_id=APP_ID,
    secret_key=SECRET_KEY,
    redirect_uri=REDIRECT_URI,
    response_type="code",
    grant_type="authorization_code"
)

# Generate login URL
auth_url = session.generate_authcode()

# Open browser automatically
webbrowser.open(auth_url)

print("Browser opened for FYERS login")

# Paste auth code
auth_code = input("Paste auth code here: ")

session.set_token(auth_code)

response = session.generate_token()

print(response)
