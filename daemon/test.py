

a = IRCBot("YoStevoBot")
a.start()

b = IRCBot("YojimboBot")
b.start()

print "ohai"

import time
time.sleep(60)

print "done"
a.stop()
b.stop()

while 1:
    pass

