import dbus

bus = dbus.SessionBus()
service = bus.get_object('com.excid3.bothost', '/com/excid3/bothost')
update = service.get_dbus_method('shutdown', 'com.excid3.bothost')
update()
