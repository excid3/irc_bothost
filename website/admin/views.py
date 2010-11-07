#from django.http import HttpResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.admin.views.decorators import staff_member_required

import dbus

@staff_member_required
def admin_dashboard(request):
    t = loader.get_template("admin/admin.html")
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))

@staff_member_required
def admin_shutdown(request):
    """shutdown the bot service"""
    try:
        bus = dbus.SessionBus()
        service = bus.get_object('com.excid3.bothost', '/com/excid3/bothost')
        update = service.get_dbus_method('shutdown', 'com.excid3.bothost')
        update()
    except dbus.DBusException, e:
        pass

    return HttpResponseRedirect("/bot-admin")
