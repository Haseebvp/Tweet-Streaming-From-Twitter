from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from tasks import start_task
from models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
import nltk
import re
import itertools
# Create your views here.


def test_async(request):
    start_task.delay()
    return render(request,'home.html')

@csrf_exempt
def load_tweets(request):
    tweet_collection = SampleCount.objects.all()
    paginator = Paginator(tweet_collection, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        tweets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tweets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tweets = paginator.page(paginator.num_pages)

    return render_to_response('home.html', {"tweets": tweets})

@csrf_exempt
def most_popular(request):
    out = []
    tweet_collection = SampleCount.objects.all()
    for tweet in tweet_collection:
        para = re.sub(r'[^\w]', ' ', tweet.text)
        s = nltk.word_tokenize(para)
        # print s
        if 'http' in s:
            s = s[:s.index('http')]
        elif ':' in s:
            s = s[s.index(':'):]
        elif 'http' in s and s[3] == ':':
            s = s[4:s.index('http')]
        else:
            s = s
        st = nltk.pos_tag(s)
        noun_list = [word for word,pos in st if pos == 'NN' or pos == 'NNP']
        noun_list = [word for word in noun_list if word.lower() != 'haircut' and len(word) > 2]
        out.append(noun_list)
    out = list(itertools.chain(*out))
    wordcount = {}
    for word in out:
        if word in wordcount:
            wordcount[word] += 1
        else:
            wordcount[word] = 1
            
    sortedbyfrequency =  sorted(wordcount,key=wordcount.get,reverse=True)
    popular = sortedbyfrequency[0:4]
    return render_to_response('home1.html',{'popular': popular})    


