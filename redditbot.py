import random
import praw 
import urllib.request
import os
from PIL import Image

class RedditBot:
    def __init__(self, username, password, secret, id, default_sub='memes'):
        # Initialise the cache
        self.cache = set()

        # Authenticate with reddit
        self.reddit = praw.Reddit(
            client_id=id,
            client_secret=secret,
            password=password,
            user_agent='Redditbot',
            username=username
        )

        # Set the bot to be only able to read posts
        self.reddit.read_only = True

        # Set the default subreddit to r/memes
        self.subreddit = self.reddit.subreddit(default_sub)

        # Load the memes into cache
        self.load_meme()

    def sub_exist(self, name: str) -> bool:
        try:
            self.reddit.subreddits.search_by_name(name, exact=True)
        except:
            return False
        else:
            return True

    def set_subreddit(self, subreddit: str) -> bool:
        """Set the subreddit for the reddit bot"""
        # Validate the validity of the subreddit
        if self.sub_exist(subreddit):
            if subreddit != self.subreddit.display_name:
                # Change the subreddit
                self.subreddit = self.reddit.subreddit(subreddit)
                print("Subreddit changed to", subreddit)

                # Reset the cache to be loaded again later when memes are fetched
                self.cache = set()
                self.load_meme()
                return True
        return False

    def load_cache(self):
        print("Loading Cache")
        
        # Get the 25 posts from the subreddit based on the 3 categories and add them to cache
        memes = [self.subreddit.hot(limit=3),self.subreddit.top(limit=3),self.subreddit.new(limit=14)]
        self.cache = self.cache.union(*map(lambda x: set(map(lambda y : y.url, x)), memes))

        # If the cache is stll empty, then the subreddit is empty
        if len(self.cache) == 0:
            print('Empty sub')
            return False
        
        # Else the cache is successfully reloaded
        print('Cache Loaded')
        return True

    def load_meme(self) -> bool:
        """Return the image file for the meme"""
        
        # If the cache is empty, fetch the memes
        if not len(self.cache):
            self.load_cache()

        # Choose a random post from the cache
        post = random.sample(self.cache, 1)[0]

        # Remove the current post from the cache
        self.cache.discard(post)

        # Check if the temp folder exists
        if not os.path.isdir('temp'):

            # If it does not exist make the ath
            os.mkdir('temp')
        
        try:
            # Open the URL and store the meme to temp/temp.png
            with urllib.request.urlopen(post) as url:
                with open('temp/temp.png', 'wb') as file:
                    file.write(url.read())

        except ConnectionError as exp:
            print("There was a connection error:", exp)
        
        except PermissionError as exp:
            print("There was a permission error:", exp)

        except Exception as exp:
            print("Something went wrong: ", exp)
            self.load_meme()

        else:
            print('Meme fetched')
            try:
                Image.open('temp/temp.png')
            except Exception as exp:
                print(exp)
                self.load_meme()
            return True
                
        return False


def main():
    """Main function to test the bot"""
    pass

# Run the main command when the file is run as the main
if __name__ == '__main__':
    main()
