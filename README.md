## Overview
I developed this bot as a personal project. It searches for the latest post containing giveaway-related keywords, saves its ID to `processed_posts.txt` for tracking (only for the first post in each run), and then uses the post's timestamp to search in descending order.

On future runs, it will continue searching in descending order until it finds the last processed post ID from `processed_posts.txt`. However, during the first run, it will continue until manually stopped.

### Features
- Searches for giveaway posts based on chosen keywords.
- Filters posts based on specified keywords.
- Performs actions based on the post's content (Like/Follow/Repost).
- Built-in check to prevent joining the same giveaways multiple times.
- Built-in rate limit checks to avoid exceeding hourly and daily API limits.
- Visual indicators/messages to confirm that everything is working correctly.

## Limits
This bot uses the free Bluesky API, which imposes hourly and daily rate limits. You can read more about them [here](https://docs.bsky.app/docs/advanced-guides/rate-limits).

At the time of writing, the API allows `5000 points` per hour and `35000 points` per day. Each "creation action" (e.g., Like, Repost, Follow) costs `3 points`. In the worst-case scenario where the bot performs all actions on every post, this means:
- **Hourly limit**: `5000 ÷ 9 ≈ 555` posts
- **Daily limit**: `35000 ÷ 9 ≈ 3888` posts

To stay within safe limits, I set the bot to process a maximum of **300 posts per hour** and **3000 posts per day**. You can adjust these values in the code if needed.

## Requirements
- **Python** (Developed with version 3.13.0)
- **Dependencies** (Install with the following command)

```sh
pip install -r requirements.txt
```

## Setup
You need a Bluesky account to obtain credentials for the bot. Your account username and password are required.

To create an app password, navigate to:
**Settings** → **Privacy & Security** → **App Passwords** → **Add App Password**

I've included a separate Python script, `auth_test.py`, to verify that your app password works before using it with the bot.

## Demo
<div align="center">
  <img src="https://github.com/user-attachments/assets/25a53917-0137-443e-81b8-44f968453034" alt="examplegif">
  <p>Example run</p>
</div>
