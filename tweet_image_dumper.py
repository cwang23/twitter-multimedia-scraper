# Program to scrape twitter photos, text, and usernames
# May 2016
# authors: Clara Wang with significant amount of code taken from source code
# source code: https://gist.github.com/freimanas/39f3ad9a5f0249c0dc64
# NOTE: if there are NO tweets associated with a Twitter handle, no CSV will be produced


import tweepy #https://github.com/tweepy/tweepy
import csv
import urllib


# Consumer keys and access tokens, used for OAuth
consumer_key = "ENTER CONSUMER KEY"
consumer_secret = "ENTER CONSUMER SECRET"
access_key = "ENTER ACCESS KEY"
access_secret = "ENTER ACCESS SECRET"


def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method

    print screen_name

    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []

    #initialize a list to hold

    #make initial request for most recent tweets (200 is the maximum allowed count)
    #if the handle is broken or doesn't exist, exit the function
    try:
        new_tweets = api.user_timeline(screen_name=str(screen_name), count=1)
    except tweepy.TweepError:
        return True


    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    if len(alltweets) > 0:
        oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)

        #all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=str(screen_name), count=200, max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one; if no tweets indicate so
        try:
            oldest = alltweets[-1].id - 1
            print "...%s tweets downloaded so far" % (len(alltweets))
        except IndexError:
            print "no tweets" + str(screen_name)


    #go through all found tweets and remove the ones with no images
    outtweets = [] #initialize master list to hold our ready tweets

    # only scrape tweets if there are tweets
    if len(alltweets) > 0:
        iteration = 1
        for tweet in alltweets:
            #not all tweets will have media url, so lets skip them
            try:
                print tweet.entities['media'][0]['media_url']
            except (NameError, KeyError):
                #we dont want to have any entries without the media_url so lets do nothing
                pass
            else:
                #got media_url - means add it to the output
                outtweets.append([tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet.entities['media'][0]['media_url']])

                # download image using media_url
                imgurl = tweet.entities['media'][0]['media_url']
                imgname = str(screen_name) + str(iteration) + ".jpg"
                try:
                    urllib.urlretrieve(imgurl, imgname)
                except IOError:
                    print screen_name
                    break
                iteration += 1


    #write the csv
    if len(outtweets) > 0:
        with open('%s_tweets.csv' % screen_name, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(["id","created_at","text","media_url"])
            writer.writerows(outtweets)

    pass

