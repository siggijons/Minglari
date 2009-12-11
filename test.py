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
    action = str(raw_input(''))
    if action == 'd':
        if not a.dead:
            a.disconnect()
        if not b.dead:
            b.disconnect()
        break
    
    elif action == '1':
        msg = str(raw_input('Talk to 1: '))
        print "You as", b.name , ": ", msg
        b.talk(msg)

    elif action == '2':
        msg = str(raw_input('Talk to 2: '))
        print "You as", a.name , ": ", msg
        a.talk(msg)
        
    elif action == '3':
        msg = str(raw_input('Talk to both: '))
        print "You as both: ", msg
        a.talk(msg)
        b.talk(msg)
        
    elif action == 'c': 
        a.connect()
        b.connect()
        
    time.sleep(5)