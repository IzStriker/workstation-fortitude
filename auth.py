import base64

def encode_credentials(username: str, password: str):
    creds = username + ":" + password
    return base64.b64encode(creds.encode('ascii')).decode('ascii')