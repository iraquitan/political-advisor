from django.shortcuts import render
from redis import Redis

redis = Redis(host='redis', port=6379)


# Create your views here.
def home(request):
    context = dict()
    counter = redis.incr('counter')
    context['counter'] = counter
    return render(request=request, template_name='myapp/home.html',
                  context=context)
