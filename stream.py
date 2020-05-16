import tweepy, json, info

class Listener(tweepy.StreamListener):

    def on_status(self, status):
        if status.user.id == 1261280540503822341:
            with open("tweet.json","r") as f:
                database  = json.load(f)

            database["new_tweet"] = True
            database["tweet"] = status.text
            
            with open("tweet.json","w") as f:
                    json.dump(database,f)

            return True

    def on_error(self, status_code):
        if status_code == 420:
            return False


class Stream():

    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth, listener=listener)

    def start(self):
        self.stream.filter(follow=["1261280540503822341"])


listener = Listener()

auth = tweepy.OAuthHandler(info.api_key, info.api_secret)
auth.set_access_token(info.access_token, info.access_secret)

stream = Stream(auth, listener)
stream.start()
