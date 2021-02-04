import tweepy 
import time
ciao = True

consumer_key = 'cJGILwxzmlcr59Jbkwta9O0nM' 
consumer_secret = 'FYplFtMriP5rxOySgnBMfM4rAlzlST9v19fGzVF3RoeGULgGSe' 
access_token = '1356642176021708802-6m6Y1W4SE4tTv8K4i0pS8vYILCXNYH' 
access_token_secret = 'VSloJBx85qUKBTuBAPhaKnB0VMouQEpZhz2GBBnrzsOCr' 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

tweetlist = ['Hello Twitter!', "Hello Twitter?", "Hello Twitter"]
print("Writing on twitter... \n")

for line in tweetlist: 
    api.update_status(line)
    print(line)
    print('...')
    time.sleep(3) 

print("All done!")