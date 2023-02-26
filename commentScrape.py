import praw
import json
import os
import datetime
import environSetting

# Get Reddit API credentials from environment variables
client_id = str(os.environ.get('REDDIT_CLIENT_ID'))
client_secret = str(os.environ.get('REDDIT_CLIENT_SECRET'))
username = str(os.environ.get('REDDIT_USERNAME'))
password = str(os.environ.get('REDDIT_PASSWORD'))


# Create a Reddit instance with your API credentials
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     username=username,
                     password=password,
                     user_agent='Baseball user comment scrape script v1.0 ; called by u/sharpShootr')


def userScrape(userString):

    # Set the Reddit username to scrape comments from
    user = reddit.redditor(userString)

    # Set the time range to scrape comments from
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365*2)

    # Retrieve the user's comments from the specified time range
    comments = [comment.body for comment in user.comments.new(limit=None) if comment.created_utc >= start_date.timestamp()]

    # Cache the comments in a JSON file
    cache_file = '{}_comments_cache.json'.format(userString)
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache = json.load(f)
    else:
        cache = {}
    cache[user.name] = comments
    with open(cache_file, 'w') as f:
        json.dump(cache, f)
    
    return cache_file


userScrape('sharpShootr')

