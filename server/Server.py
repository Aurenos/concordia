#!/usr/bin/env python

from asyncore import dispatcher
from asynchat import async_chat
#from apiclient.discovery import build
from ServerCommands import *
import socket, asyncore

PORT = 1338
NAME = "Concordia"
MOTD = "Welcome to the Concordia chat server! Please keep in mind that the Google Translate API costs money for us to use. So don't go overboard with this...or I'll find you."

# Google API Key for authorizing Google Apps transactions
G_API_KEY = ''

class ChatSession(async_chat):
    def __init__(self, server, sock):
        async_chat.__init__(self, sock)
        self.server = server
        self.set_terminator("\r\n")
        self.data = []
        self.text_received = ""
        self.nick = ""
        self.language = "en"

    def collect_incoming_data(self, data):
        self.data.append(data)

    def found_terminator(self):
        line = ''.join(self.data[-1])
        print line
        print len(self.data)
        if len(self.data) > 1:
        	print len(self.data[0]), len(self.data[1]), len(self.data[2])
        self.data = []
        if not line.startswith('/'):
            self.server.broadcast(1, line, username=self.nick, lang=self.language)
        elif line == "":
            pass
        else:
            if not line == '/':
                cmdmsg = line[1:].split()
                cmd = cmdmsg[0]
                if COMMANDS.has_key(cmd):
                    COMMANDS[cmd](self, cmdmsg)
                else:
                    self.server.send_private_message(self, "Command: " + cmd + " NOT FOUND")

            
    def handle_close(self):
        async_chat.handle_close(self)
        self.server.disconnect(self)
        
class ChatServer(dispatcher):
    def __init__(self, port, name):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)
        self.sessions = []
        
        self.service = build('translate', 'v2', developerKey=G_API_KEY)

    def disconnect(self, session):
        print session.nick,"has disconnected"
        self.sessions.remove(session)
    
    def send_motd(self, session):
    	print (MOTD + '\r\n')
        session.push((MOTD + '\r\n'))
        
    def send_private_message(self, session, msg):
        session.push((msg + '\r\n'))
    
    ###     Message Types    ###
    # Server message = 0
    # User message = 1       
    ############################
    
    def broadcast(self, msg_type, msg, username="", lang=""):
        if msg_type == 0:
            for session in self.sessions:
                session.push((msg + '\r\n'))
        elif msg_type == 1:
            for session in self.sessions:
                trans = msg
                print "'"+trans+"'"
                if session.language != lang:
                    translation = self.service.translations().list(
                        source=lang,
                        target=session.language,
                        q=[msg]
                    ).execute()
                    trans = translation['translations'][0]['translatedText']
                message = username + '>> ' + trans + '\r\n'
                print "Message:",message
                session.push(message)
        else:
            print "Invalid message type:",msg_type,"for method BROADCAST"

    def handle_accept(self):
        conn, addr = self.accept()
        self.sessions.append(ChatSession(self, conn))
        self.sessions[-1].nick = str(addr[0])
        print self.sessions[-1].nick,"has connected"
        self.send_motd(self.sessions[-1])

if __name__ == '__main__':
    with open('api_key.txt') as f:
        G_API_KEY = f.readline()
    s = ChatServer(PORT, NAME)
    print "Waiting for client connections"
    try: asyncore.loop()
    except KeyboardInterrupt: print "Server stopped."
