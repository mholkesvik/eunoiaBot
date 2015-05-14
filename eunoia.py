#!/usr/bin/python
import twitter
import time
import datetime
import random

api = twitter.Api(
    consumer_key='TNjP4JEhmq8iqOqc4x2jrsbIj', 
    consumer_secret='NwpPFvt7D6MWLjUSNuDctudWCwLwrGOZ2Tey4obiyTqEOgLCNq', 
    access_token_key='2426543023-tZlsWuXsyan2BKjuvZkjExIOP4zdOZAkkE1DkId', 
    access_token_secret='PQRR7gJqd2oIyCGAjOhRJd9keljHEayj5bpmqaHL5wMsv'
)

def isEunoia(text):
    vowels = "aeiou"
    firstVowel = ''
    for char in text.lower():
        if char == 'y':
            return False
        if char in vowels:
            if firstVowel == '':
                firstVowel = char
            elif char != firstVowel:
                return False
    # we want at least 1 vowel
    return True if char != '' else False


# bad.txt contains the most common english 
# words in Eunoia violation
def getBadWords():
    with open('bad.txt','r') as f:
        allBadWords = f.read().split('\n')
        selectBadWords = random.sample(set(allBadWords), 30)
        return "-" + " -".join(selectBadWords)


# good.txt contains some of the most common 
# english words _not_ in Eunoia violation
def getGoodWords():
    with open('good.txt','r') as f:
        allGoodWords = f.read().split('\n')
        randomGoodWords = random.sample(set(allGoodWords), 4)
        return " ".join(randomGoodWords)


def getTweets():
    results = []
    badWords = getBadWords()
    goodWords = getGoodWords()

    # Twitter API enforces that you include at least one word you want
    for goodWord in goodWords.split( ):
        results.extend(api.GetSearch(
                            term = goodWord + badWords
                            ,count=100
                            ,lang='en')
        )
    print "Total of " + str(len(results)) + " results found!"
    return results


def parseResults(results):
    for tweet in results:
        encodedTweetText = tweet.text.encode("utf-8")
        if isEunoia(encodedTweetText):
            print '---------------------'
            print encodedTweetText
            print "https://twitter.com/"+ tweet.user.screen_name + "/status/" + str(tweet.id)


if __name__ == "__main__":
    print "---- New Run ----"
    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    parseResults(getTweets())