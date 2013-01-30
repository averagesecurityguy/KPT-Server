import requests
import oauth


class Twitter():
    def __init__(self):
        # DO NOT PUBLISH THIS
        self.consumer_key = '8TWQ06iBk4VOOM9LCS7y2A'
        self.consumer_secret = 'aCiGzWJTGj2tuzcCP2rVg5vbBjYpOj9PHUHodfG6iQ'
        self.token = '244128388-92GrVdq34lCInFHtdPtZUV7ktaMcvfUBxvUoAv54'
        self.token_secret = 'o92OSJsBpIegy0bQmGTSzknZDm0Pv5ty8awMrGsPQw'
        self.__base = 'https://api.twitter.com/1.1'
        self.__ssn = requests.Session()
        self.__ssn.auth = oauth.TwitterSingleOAuth(self.consumer_key,
                                                   self.consumer_secret,
                                                   self.token,
                                                   self.token_secret)

    def get_mentions(self):
        r = self.__ssn.get(self.__base + '/statuses/mentions_timeline.json')

        mentions = []
        for t in r.json():
            for a in t:
                print u'{0}: {1}\a'.format(a, t[a])

            m = u"{0} ({1}) - {2}".format(t['user']['screen_name'],
                                         t['user']['name'],
                                         t['text'])
            mentions.append(m)

        return mentions


if __name__ == '__main__':
    t = Twitter()

    print '\n'.join(t.get_mentions())
