from mingle import MingleClient, MingleThread
import time

a = MingleClient("Stranger1")
b = MingleClient("Stranger2")

a.setStranger(b)
b.setStranger(a)

a.connect()
b.connect()

t = MingleThread(a)
t.start()

u = MingleThread(b)
u.start()

while True:
    msg = str(raw_input(''))
    if msg == 'd':
        a.disconnect()
        b.disconnect()
        break
        
#    if a.dead:
#        a.connect()
#    if b.dead:
#        b.connect()
        
    time.sleep(5)