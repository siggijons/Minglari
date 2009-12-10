import threading
import time
import urllib2 as url
import urllib
import json
from StringIO import StringIO

class MingleThread( threading.Thread ):
    
    def __init__(self, client):    
        self.client = client
        threading.Thread.__init__(self)
    
    def run(self):
        # Fetch events from server
        while True:
            starttime=time.clock()
            
            site = url.urlopen(self.client.req)
            rec = site.read()
            self.handleEvents(rec)
            
            if (c.dead):
                break
            
            stoptime=time.clock()
            print "* events: %.3f seconds" % (stoptime-starttime)
            
            time.sleep(2)
    
    def handleEvents(self, events):
        io = StringIO(events)
        j = json.load(io)
        
        if (type(j).__name__ == 'list'):
            for event in j:
                self.handleEvent(event)
        else:
            print "* Could not parse events"
            print events
            
    def handleEvent(self, event):
        if len(event) > 0:
            action = event[0]
            
            if action == "waiting":
                print "Looking for someone you can chat with. Hang on."

            elif action == "connected":
                print "You're now chatting with a random stranger. Say hi!"

            elif action == "gotMessage":
                print "Stranger: " , event[1]

            elif action == "strangerDisconnected":
                print "Your conversational partner has disconnected."
            
            elif action == "typing":
                print "Stranger is typing..."

            elif action == "stoppedTyping":
                print "Stranger stopped typing..."
                
            else:
                print "** Unknown event"
                print event
            
        

class MingleClient():
    def connect(self):
        # Connect and get our id
        site = url.urlopen('http://omegle.com/start','')
        r = site.read()
        self.id = r[1:len(r)-1]
        self.dead = False
        print "id: ", self.id
        
        # Create request object for events
        self.req = url.Request('http://omegle.com/events', urllib.urlencode( {'id':self.id}))
    
    def talk(self):        
        action = str(raw_input('* a:'))
        
        if (action == 'd'):
            self.dead = True
            r = url.urlopen('http://omegle.com/disconnect', '&id='+self.id)
            print "Disconnected"
            print r.read()
            
        elif (action == 't'):
            typing = url.urlopen('http://omegle.com/typing', '&id='+self.id)
            typing.close()
            
            msg = str(raw_input('* t: '))
            
            print "You: " , msg
            r = url.urlopen('http://omegle.com/send', '&msg='+msg+'&id='+self.id)
            r.close()
            
        else:
            print "unknown command. Use d to disconnect, and t to chat"


if __name__ == '__main__':
    c = MingleClient()
    c.connect()
    
    t = MingleThread(c)
    t.start()
    
    while True:
        c.talk()
        if (c.dead):
            break
    
    
    