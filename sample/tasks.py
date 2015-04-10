from models import SampleCount
from celery.decorators import task
from twython import TwythonStreamer


class TweetStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            text =  data['text'].encode('utf-8')
            new = SampleCount()
            #print new.count
            new.text = text
            new.save()


    def on_error(self, status_code, data):
        print status_code, data
        #self.retry()



@task(bind=True, default_retry_delay=30 * 60)
def start_task(self):
    APP_KEY = 'gfgM72294MAzOJXWqsVfSTz5t'
    APP_SECRET = 'kJfXilS37KwbMzO97VDPSbIyqCEK7cc6m6PkzzZ6xoc3r9E6Xi'
    OAUTH_TOKEN = '2583670422-znj1gptwrYPyIucepRIhJF9HTwjCyCMlC39TCGF'
    OAUTH_TOKEN_SECRET = 'TdVsvnP9gtHS8VR9rwHy2ICgFFre2bEHdkYI7jwTD4djR'

    try:
        stream = TweetStreamer(APP_KEY, APP_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        stream.statuses.filter(track='haircut')
    except Exception as exc:
        raise self.retry(exc=exc, countdown=30)