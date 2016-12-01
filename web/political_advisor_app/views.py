from django.shortcuts import render
from redis import Redis

redis = Redis(host='redis', port=6379)


# Create your views here.
def home(request):
    counter = redis.incr('counter')
    return render(request, 'political_advisor_app/home.html',
                  {'counter': counter})
