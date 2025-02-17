import requests

# Base URL for the API
BASE_URL = "https://bsky.social/xrpc"

# Your credentials
USERNAME = "name.bsky.social"  # Replace with your Bluesky username
PASSWORD = "ssss-mmmm-uuuu-gggg"  # Replace with the app password you generated

def authenticate():
    """Authenticate with the Bluesky API and return the access token."""
    response = requests.post(f"{BASE_URL}/com.atproto.server.createSession", json={
        "identifier": USERNAME,
        "password": PASSWORD
    })
    if response.status_code == 200:
        data = response.json()
        print("Authentication successful!")
        print("Access Token:", data['accessJwt'])
        return data['accessJwt']
    else:
        print("Authentication failed:", response.json())
        return None

# Test authentication
if __name__ == "__main__":
    authenticate()