import requests
import time
import random
from atproto import Client

# Base URL for the API
BASE_URL = "https://bsky.social/xrpc"

# Credentials
USERNAME = "name.bsky.social" # Replace with your Bluesky username
APP_PASSWORD = "ssss-mmmm-uuuu-gggg" # Replace with the app password you generated
USER_PASSWORD = "pass12345" # Replace with your account password

# Access token from authentication
ACCESS_TOKEN = None

# Path to save processed post URIs
PROCESSED_FILE = 'processed_posts.txt'

# AUTHENTICATE --------
def authenticate():
    """Authenticate with the Bluesky API and return the access token."""
    global ACCESS_TOKEN
    response = requests.post(f"{BASE_URL}/com.atproto.server.createSession", json={
        "identifier": USERNAME,
        "password": APP_PASSWORD
    })
    if response.status_code == 200:
        data = response.json()
        print("Authentication successful!")
        ACCESS_TOKEN = data['accessJwt']
        return True
    else:
        print("Authentication failed:", response.json())
        return False

# CHECK POST IN LIST
def is_processed(uri):
    try:
        with open(PROCESSED_FILE, 'r') as file:
            processed_uris = file.read().splitlines()
        return uri in processed_uris
    except FileNotFoundError:
        return False

# SAVE POST IN LIST
def save_processed_uri(uri):
    with open(PROCESSED_FILE, 'a') as file:
        file.write(uri + '\n')

# SEARCH ------------------
def search_posts(keyword, until=None):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {
        "q": keyword,
        "sort": "latest",
        "limit": 1  # Always fetch one post
    }
    if until:
        params['until'] = until

    try:
        response = requests.get(f"{BASE_URL}/app.bsky.feed.searchPosts", headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            posts = data.get('posts', [])
            return posts[0] if posts else None  # Return the single post or None
        else:
            print(f"Search failed with status {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error during search_posts: {e}")
        return None

def is_filtered(post):
    CASE_SENSITIVE_FILTER = ['US', 'U.S.', 'OC']
    CASE_INSENSITIVE_FILTER = ['art', 'sketch', 'screenshot']

    text = post.get('record', {}).get('text', '')

    if any(mention in text for mention in CASE_SENSITIVE_FILTER):
        return True
    if any(link in text.lower() for link in CASE_INSENSITIVE_FILTER):
        return True
    
    return False

# INTERACT -------------
def interact_with_post(post):
    """Interact with the post based on the keywords present in the text."""
    text = post.get('record', {}).get('text', '').lower()
    print(f"Post Content:\n\n{text}\n")

    if "like" in text:
        like_post(post['uri'], post['cid'])

    repost_keywords = ["repost", "reskeet", "rt", "retweet", "share"]
    if any(keyword in text for keyword in repost_keywords):
        repost_post(post['uri'], post['cid'])

    if "follow" in text:
        follow_user(post['author']['did'])

# LIKE -----------------
def like_post(post_uri, post_cid):
    try:
        response = client.like(uri=post_uri, cid=post_cid)
        print(f"❤️ Liked post successfully.")
        time.sleep(random.randint(4, 9))
    except Exception as e:
        print(f"Error occurred while liking post: {e}")

# REPOST ----------------
def repost_post(post_uri, post_cid):
    try:
        response = client.repost(uri=post_uri, cid=post_cid)
        print(f"🔄 Reposted post successfully.")
        time.sleep(random.randint(5, 10))
    except Exception as e:
        print(f"Error occurred while reposting post: {e}")

# FOLLOW ---------------
def follow_user(did):
    try:
        response = client.follow(subject=did)
        print(f"➕ Followed user successfully.")
        time.sleep(random.randint(6, 11))
    except Exception as e:
        print(f"Error occurred while following user: {e}")

# MAIN =================
if __name__ == "__main__":
    if authenticate():
        client = Client()
        client.login(USERNAME, USER_PASSWORD)

        keyword = "giveaway like follow"
        last_timestamp = None
        interacted_count = 0
        cycles = 0

        while True:
            if not last_timestamp:
                post = search_posts(keyword)
                if post:
                    last_timestamp = post.get('record', {}).get('createdAt')
                    if not is_processed(post['uri']):
                        save_processed_uri(post['uri'])
                        interacted_count += 1
                        print(f"✨New post found! ✨Total number: {interacted_count} ✨Cycles: {cycles}")
                        
                        if interacted_count >= 300:
                            cycles += 1
                            interacted_count = 0
                            print(f"✨Reached 300 posts! Pausing for 1 hour...")
                            time.sleep(3600)
                        
                        if cycles >= 10:
                            print("✨Reached limit for the day. Stopping the bot.")
                            break

                        if not is_filtered(post):
                            interact_with_post(post)
                        else:
                            print("🛑Filtered post due to restricted keywords.")
                    else:
                        print("❌No older posts found. Restarting initial search after 10 minutes.")
                        time.sleep(600)
                        last_timestamp = None
                else:
                    print("❌No recent posts found.")
            else:
                post = search_posts(keyword, until=last_timestamp)
                if post:
                    if not is_processed(post['uri']):
                        last_timestamp = post.get('record', {}).get('createdAt')
                        interacted_count += 1
                        print(f"✨New post found! ✨Total number: {interacted_count} ✨Cycles: {cycles}")
                        
                        if interacted_count >= 300:
                            cycles += 1
                            interacted_count = 0
                            print(f"✨Reached 300 posts! Pausing for 1 hour...")
                            time.sleep(3600)
                        
                        if cycles >= 10:
                            print("✨Reached limit for the day. Stopping the bot.")
                            break

                        if not is_filtered(post):
                            interact_with_post(post)
                        else:
                            print("🛑Filtered post due to restricted keywords.")
                    else:
                        print("❌No older posts found. Restarting initial search after 10 minutes.")
                        time.sleep(600)
                        last_timestamp = None
                else:
                    print("❌No older posts found. Restarting initial search after 10 minutes.")
                    time.sleep(600)
                    last_timestamp = None

            print("Waiting before next search...")
            time.sleep(random.randint(7, 12))
