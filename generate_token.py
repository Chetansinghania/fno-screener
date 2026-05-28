from fyers_apiv3 import fyersModel
from urllib.parse import urlparse, parse_qs

client_id = "G5H4DU2N1A-100"
secret_key = "3CXN9E40BC"
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"

session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type="code",
    grant_type="authorization_code"
)

login_url = session.generate_authcode()

print("\nOPEN THIS URL IN BROWSER:\n")
print(login_url)

redirected_url = input("\nPASTE FULL REDIRECTED URL AFTER LOGIN:\n")

parsed = urlparse(redirected_url)

auth_code = parse_qs(parsed.query)["auth_code"][0]

session.set_token(auth_code)

response = session.generate_token()

print("\nACCESS TOKEN:\n")

print(response["access_token"])