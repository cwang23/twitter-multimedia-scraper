# author Clara Wang
# program to download tweeted images from Twitter
# May 2016

import csv
import time
import os
from tweet_image_dumper import get_all_tweets


# set working directory
# Clara's wd: "C:/Users/Clara/Desktop/f001c1f/Pres Scholars Research/India Project/scraped"
os.chdir("ENTER WORKING DIRECTORY HERE")


# function to read list of twitter handles from csv
def create_userlist(csvfile):
    usernames = []
    file = open(csvfile, "rb")
    csv_users = csv.reader(file)
    for row in csv_users:
        usernames.append(row)
    file.close()
    return usernames


# list of Indian politician Twitter handles
handles = create_userlist("ENTER NAME OF CSV FILE CONTAINING TWITTER HANDLES HERE (i.e. 'usernames.csv')")
# csv files are: highofficers.csv, partyleaders.csv, statechiefministers.csv, loksabha.csv


# code sleeps for 15 minutes after every 8 usernames so we don't exceed Twitter API rate limit (resets every 15 min)
iteration = 0
broken_handles = []  # list of broken handles
for handle in handles:
    # if handle doesn't exist, skip over and add to list of broken handles
    if get_all_tweets(handle[0]):
        broken_handles.append(handle[0])
    else:
        iteration += 1
        if iteration % 8 == 0:
            time.sleep(60 * 15)
    # print the list of broken handles at the end to see which ones failed
    print broken_handles