import tweepy
import time
from typing import List, Dict, Any
import json
import csv
import jsonpickle


st = time.time()

consumer_key = "nV211cauWjRmdu9a613t7bXON"
consumer_secret = "BhUXQCxACTexmi0Y1A7qvpLaAKrIKfnJCphlWYhjTmP33wNYkb"
access_token = "4559785366-e3uLZEyJhIxTf4Gu01s99FS1CnZ5cONLiUmyj4C"
access_token_secret =  "etuvGy3TxNjuua0NDNu1WgyfenNgauhSXtSxLRl729Qpl"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


tweetsPerQuery = 10 #this is the maximum provided by API
max_tweets = 5000 # just for the sake of While loop
fName = 'tweets.txt' # where i save the tweets
search_query=["harassment", "bullying", "intimidation", "cyberbullying", "abuse", "victimization", "discrimination", "threats", "stalking", "coercion"]







#No sinceId and max_id ..Get whathever you have exhaustively
since_id = None
max_id = -1
tweet_count = 0
print("Downloading the tweeets for Search Query..takes some time..")

x=0
with open(fName,'w') as f:
    print("Downloading hashtag")
    while(tweet_count<max_tweets):
        try:
            if(max_id<=0):
                if(not since_id):
                    new_tweets = api.search_tweets(q=search_query,count=tweetsPerQuery,tweet_mode='extended')

                else:
                    new_tweets = api.search_tweets(q=search_query,count=tweetsPerQuery,tweet_mode='extended',since_id=since_id)
            else:
                if(not since_id):
                    new_tweets = api.search_tweets(q=search_query,count=tweetsPerQuery,tweet_mode='extended',max_id=str(max_id-1))
                else:
                    new_tweets = api.search_tweets(q=search_query,count=tweetsPerQuery,tweet_mode='extended',max_id=str(max_id-1),since_id=since_id)

            # Tweets Exhausted
            if(not new_tweets):
                print("No more tweets found!!")
                break
            # write all the new_tweets to a json file
            for tweet in new_tweets:
                f.write(jsonpickle.encode(tweet._json,unpicklable=False)+'\n')
                tweet_count+=len(new_tweets)
                print("Successfully downloaded {0} tweets".format(tweet_count))
                max_id=new_tweets[-1].id
        # in case of any error
        except tweepy.errors.TweepyException as e:
                print("Some error!!:"+str(e))
                break
end = time.time()

print("A total of {0} tweets are downloaded and saved to {1}".format(tweet_count,fName))
print("Total time taken is ",end-st,"seconds.")


f = open(r'C:\Users\ASUS\Desktop\Projet_Data_Kaisens\Api\data_twitts.csv', 'a', encoding='utf-8')
csvWriter = csv.writer(f)
headers=['text']
csvWriter.writerow(headers)

for inputFile in ['tweets.txt']:#all the text-file names you want to convert to Csv in the see folder as this code
    tweets = []
    for line in open(inputFile, 'r'):
        tweets.append(json.loads(line))

    print('HI',len(tweets))
    count_lines=0
    for tweet in tweets:
        try:
            #csvWriter.writerow([tweet['id_str'],tweet['full_text'].split(":")[0],tweet['full_text'],classify_tweet(tweet['full_text'])])
            csvWriter.writerow([tweet['text']])

            count_lines+=1
        except Exception as e:
            print(e)
    print(count_lines)