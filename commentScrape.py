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

    subreddits = set(["baseball", "mlb", "Astros", "azdiamondbacks", "Braves", "Orioles", "RedSox", "Cubs", "Reds", "ColoradoRockies", "ClevelandGuardians", "WhiteSox", "motorcitykitties", "letsgofish", "KCRoyals", "AngelsBaseball", "Dodgers", "Brewers", "MinnesotaTwins", "NewYorkMets", "NYYankees", "oaklandathletics", "Phillies", "Buccos", "Padres", "Mariners", "SFGiants", "Cardinals", "TampaBayRays", "TexasRangers", "TorontoBlueJays", "Nationals"])


    # Retrieve the user's comments from the specified time range
    user_comments = {}
    for comment in user.comments.new(limit=None):
        subreddit_name = comment.subreddit.display_name
        if subreddit_name in subreddits and comment.created_utc >= start_date.timestamp() and comment.created_utc <= end_date.timestamp():
            if subreddit_name not in user_comments:
                user_comments[subreddit_name] = []
            user_comments[subreddit_name].append(comment.body)

    original_cwd = os.getcwd()
    # Cache the comments in a JSON file    
    target_directory = 'jsonFiles'
    os.chdir(target_directory)
    cache_file = '{}_comments_cache.json'.format(userString)
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache = json.load(f)
    else:
        cache = {}
    cache[user.name] = user_comments
    with open(cache_file, 'w') as f:
        json.dump(cache, f)
    os.chdir(original_cwd)
    return cache_file





