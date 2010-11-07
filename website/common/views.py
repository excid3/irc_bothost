from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from models import Bot, BOT_TYPES
import validate

import dbus
import simplejson

@login_required
def common_bot(request, id):
    """Bot overview"""
    errors = {}
    
    # If bot is public, don't filter by owner
    bot = Bot.objects.filter(id=id, owner=request.user)
    if not bot:
        errors["bot"] = "Invalid bot ID"
        
        #TODO: Render 404
        t = loader.get_template("common/bot_overview.html")
        c = RequestContext(request, locals())
        return HttpResponse(t.render(c))
        
    bot = bot[0]

    t = loader.get_template("common/bot_overview.html")
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))

@login_required
def common_edit(request, id):
    """Bot administration"""
    errors = {}
    
    bot = Bot.objects.filter(id=id, owner=request.user)
    if not bot:
        errors["bot"] = "You do not have permission to edit this bot"
        
        return HttpResponseRedirect("/")
        #t = loader.get_template("common/bot_admin.html")
        #c = RequestContext(request, locals().update(bottypes=BOT_TYPES))
        #return HttpResponse(t.render(c))

    bot = bot[0]
    
    if request.POST:
        name = request.POST.get("name")
        server = request.POST.get("server")
        type = int(request.POST.get("type"))
        channels = request.POST.get("channels")
        port = request.POST.get("port")
        
        # validate
        bot.name = name
        bot.server = server
        bot.port = port
        bot.type = type
        bot.channels = channels
        
        bot.save()
        
        return HttpResponseRedirect("/bots/%i" % bot.id)
    
    locals().update(bottypes=BOT_TYPES) 
    t = loader.get_template("common/bot_admin.html")
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))
    
@login_required
def common_delete(request, id):
    errors = {}
    
    bot = Bot.objects.filter(id=id, owner=request.user)
    if not bot:
        errors["bot"] = "You do not have permission to edit this bot"
        
        return HttpResponseRedirect("/")
        #t = loader.get_template("common/bot_admin.html")
        #c = RequestContext(request, locals().update(bottypes=BOT_TYPES))
        #return HttpResponse(t.render(c))

    # Shutdown the bot via dbus
    bus = dbus.SessionBus()
    service = bus.get_object('com.excid3.bothost', '/com/excid3/bothost')
    func = service.get_dbus_method('delete_bot', 'com.excid3.bothost')
    func(bot[0].id)

    bot[0].delete()
    
    return HttpResponseRedirect("/")
    
@login_required
def common_new(request):
    port = 6667
    if request.POST:
        name = request.POST.get("name")
        server = request.POST.get("server")
        type = int(request.POST.get("type"))
        channels = request.POST.get("channels")
        port = request.POST.get("port")
        nick = name

        # Validate
        errors = {}
        if len(name) > 36 or len(name) < 1:
            errors["name"] = "Username must be 36 characters or less"
        # test name for invalid characters
        
        if Bot.objects.filter(name=name, server=server):
            errors["name"] = "Nick already taken on %s" % server
        
        if not isinstance(type, int):
            errors["type"] = "Invalid bot type"
            
        #TODO: Regex!
        if len(server) < 5:
            errors["server"] = "Invalid server name"

        #TODO: Better checking
        if len(channels) < 1:
            errors["channels"] = "Specify at least one channel"
        elif len(channels) > 2000:
            errors["channels"] = "Too many channels specified"
           
        if len(port) > 5:
            errors["port"] = "Invalid port number, 6667 is default"
            
        if not port:
            port = 6667
        port = int(port)

        if not errors:
            bot = Bot(owner=request.user, name=name, nick=nick, server=server, port=port, type=type, channels=channels, status=0)
            bot.save()

#            args = (type, bot.owner_id, name, server, port, channels)
            args = (server, port, nick, channels)

            # Create the bot on the daemon
            bus = dbus.SessionBus()
            service = bus.get_object('com.excid3.bothost', '/com/excid3/bothost')
            new_bot = service.get_dbus_method('new_bot', 'com.excid3.bothost')
            new_bot(type, bot.id, args)

            #TODO: Display a "successfully created" message at the top of the dashboard
            return HttpResponseRedirect("/")

    locals().update(bottypes=BOT_TYPES)            
    t = loader.get_template("common/new.html")
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))
    
def common_update(request):
    """returns a json response with all the updates by bot_id keys"""
    # { id#: [(type, args), (type, args)] }
    json_update_dict = {}
    for bot in Bot.objects.all():
        bot_updates = []
        for update in Update.objects.filter(bot=bot):
            bot_updates.append((update.type, 
                            [x.strip() for x in update.arguments.split(",")]))
        json_update_dict[bot.id] = bot_updates
    
    json = simplejson.dumps(json_update_dict, 
                              default=lambda o: {o : str(json_update_dict[o]) })

    # Example: www.example.com/updates?format=json
    format = request.GET.get("format")
    if format == "json":
        return HttpResponse(json, mimetype="application/json")
    #elif format == "xml":
    #   return HttpResponse XML version of json
    
    return HttpResponse(json)
