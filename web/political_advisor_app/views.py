from django.shortcuts import render
from redis import Redis

redis = Redis(host='redis', port=6379)


# Create your views here.
def home(request):
    counter = redis.incr('counter')
    return render(request, 'home.html', {'counter': counter})
