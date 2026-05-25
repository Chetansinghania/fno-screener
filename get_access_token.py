from fyers_apiv3 import fyersModel

client_id = "1N48IQB7GQ-100"
secret_key = "7TX0ILW68X"

auth_code = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBfaWQiOiIxTjQ4SVFCN0dRIiwidXVpZCI6IjM5NDZjNzhiNWI4MTRhYTQ4MjU1ZDg2NDg0ZjIxMDEyIiwiaXBBZGRyIjoiIiwibm9uY2UiOiIiLCJzY29wZSI6IiIsImRpc3BsYXlfbmFtZSI6IlhDMDgxNjEiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI1ZjhjYTgwMDA0YmRlMThhN2NkMDNmZjY2ZGU4NDM5OTkzNGQ1MGI4MmE0MDJhZmI4MzU4NDYzMCIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImF1ZCI6IltcImQ6MVwiLFwiZDoyXCIsXCJ4OjBcIixcIng6MVwiLFwieDoyXCJdIiwiZXhwIjoxNzc5NjQ1Nzk4LCJpYXQiOjE3Nzk2MTU3OTgsImlzcyI6ImFwaS5sb2dpbi5meWVycy5pbiIsIm5iZiI6MTc3OTYxNTc5OCwic3ViIjoiYXV0aF9jb2RlIn0.tCrqVv1CRcgQl-cp9jF2oJ-OeX-by9AG2sT-oRHK-O8"

session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri="https://127.0.0.1",
    response_type="code",
    grant_type="authorization_code"
)

session.set_token(auth_code)
response = session.generate_token()

print(response)
