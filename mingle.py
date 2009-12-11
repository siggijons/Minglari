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
            
            if (self.client.dead):
                break
            
            stoptime=time.clock()
            #print "* events: %.3f seconds" % (stoptime-starttime)
            
            time.sleep(3)
    
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
                print "*", self.client.name, "Looking for someone you can chat with. Hang on."

            elif action == "connected":
                print "*", self.client.name, "You're now chatting with a random stranger. Say hi!"

            elif action == "gotMessage":
                if self.client.stranger:
                    self.client.stranger.talk(event[1])
                else:
                    print "Stranger: " , event[1]

            elif action == "strangerDisconnected":
                print "*", self.client.name, "Your conversational partner has disconnected."
                if self.client.stranger:
                    self.client.stranger.disconnect()
            
            elif action == "typing":
                #print "* Stranger is typing..."
                if self.client.stranger:
                    self.client.stranger.typing()

            elif action == "stoppedTyping":
                #print "* Stranger stopped typing..."
                if self.client.stranger:
                    self.client.stranger.stopTyping()
                
            else:
                print "*", self.client.name, "** Unknown event"
                print event
            
                
class MingleClient():
    def __init__(self, name):
        self.name = name
        self.stranger = False
    
    def setStranger(self, stranger):
        self.stranger = stranger
        
    def connect(self):
        # Connect and get our id
        site = url.urlopen('http://omegle.com/start','')
        r = site.read()
        self.id = r[1:len(r)-1]
        self.dead = False
        print "id: ", self.id
        
        # Create request object for events
        self.req = url.Request('http://omegle.com/events', urllib.urlencode( {'id':self.id}))
    
    def talk(self, msg):        
        print self.name, ": ", msg
        r = url.urlopen('http://omegle.com/send', "&" + urllib.urlencode( {'msg': msg, 'id':self.id}))
        r.close()
        
    def typing(self):
        typing = url.urlopen('http://omegle.com/typing', '&id='+self.id)
        typing.close()
    
    def stopTyping(self):
        typing = url.urlopen('http://omegle.com/stoppedtyping', '&id='+self.id)
        typing.close()

    def disconnect(self):
        self.dead = True
        r = url.urlopen('http://omegle.com/disconnect', '&id='+self.id)
        print "Disconnected"
        print r.read()
        r.close()


if __name__ == '__main__':
    c = MingleClient("You")
    c.connect()
    
    t = MingleThread(c)
    t.start()
    
    while True:
        msg = str(raw_input(''))
        
        if msg == 'd':
            c.disconnect()
        elif msg == 't':
            c.typing()
        elif msg == 'c':
            c.connect()
        else:
            c.talk(msg)
            
        if (c.dead):
            break
    
    
    