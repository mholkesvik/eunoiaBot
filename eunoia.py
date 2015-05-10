#!/usr/bin/python
import twitter
import time
import datetime

api = twitter.Api(
    consumer_key='foo', 
    consumer_secret='bar', 
    access_token_key='baz', 
    access_token_secret='bongo'
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
        return f.read().replace(' ', ' -')


# good.txt contains some of the most common 
# english words _not_ in Eunoia violation
def getGoodWords():
    with open('good.txt','r') as f:
        return f.read()


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