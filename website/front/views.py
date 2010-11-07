from django.http import HttpResponse
from django.template import RequestContext, loader
from common.models import Bot

def front_front(request):
    """This is the homepage"""

    # Simply render the homepage if user isn't logged in
    if not request.user.is_authenticated():
        t = loader.get_template('front/index.html')
        c = RequestContext(request)
        return HttpResponse(t.render(c))

    # Render the user's dashboard  
    bots = Bot.objects.all().filter(owner=request.user)
    
    t = loader.get_template('front/dashboard.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))
