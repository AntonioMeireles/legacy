"""Stomp Protocol Connectivity

    This provides basic connectivity to a message broker supporting the 'stomp' protocol.
    At the moment ACK, SEND, SUBSCRIBE, UNSUBSCRIBE, BEGIN, ABORT, COMMIT and DISCONNECT operations
    are supported.  CONNECT is implicit.
    
    This changes the previous version which required a listener per subscription -- now a listener object
    just calls the 'addlistener' method and will receive all messages sent in response to all/any subscriptions.
    (The reason for the change is that the handling of an 'ack' becomes problematic unless the listener mechanism
    is decoupled from subscriptions).
    
    UNSUBSCRIBE seems to be broken.  Can't tell if it's my fault or activemq's, but when I do it manually from
    telnet, I get the same results.

    Note that you must 'start' an instance of Connection to begin receiving messages.  For example:
    
        conn = stomp.Connection('localhost', 62003, 'myuser', 'mypass')
        conn.start()

    Meta-Data
    ---------
    Author: Jason R Briggs
    License: http://www.apache.org/licenses/LICENSE-2.0
    Version: $Revision: 1.2 $
    Start Date: 2005/12/01
    Last Revision Date: $Date: 2005/12/05 23:21 $
    
    Notes/Attribution
    -----------------
    * uuid method courtesy of Carl Free Jr:
      http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/213761

    Modifications
    -------------

    * Modified 04/2007 by rPath, Inc.
      - Fixed infinite-loop bugs when stomp server goes away.
      - Added delay between reads to avoid 100% CPU loops.
    * Modified 12/2007 by rPath, Inc.
      - If the parent thread has gone away without disconnecting, quit
        when there is no more data to send.

"""

import md5
import random
import re
import select
import socket
import sys
import threading
import time

# retrieve a description from the headers of a message
_destination_re = re.compile(r'destination:\s*(.*)')

def _uuid( *args ):
    """
    uuid courtesy of Carl Free Jr:
    (http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/213761)
    """
    
    t = long( time.time() * 1000 )
    r = long( random.random() * 100000000000000000L )
  
    try:
        a = socket.gethostbyname( socket.gethostname() )
    except:
        # if we can't get a network address, just imagine one
        a = random.random() * 100000000000000000L
    data = str(t) + ' ' + str(r) + ' ' + str(a) + ' ' + str(args)
    data = md5.md5(data).hexdigest()
  
    return data
    

class Connection(threading.Thread):
    
    def __init__(self, host, port, user='', passcode=''):
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ss.connect((host, port))
        self.rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rs.connect((host, port))
        self.rs.settimeout(1)
        self.buf = [ ]
        self.sendbuf = [ ]
        
        self.listeners = [ ]
        
        self.running = 1
        self._parent_thread = threading.currentThread()
        
        connstr = 'CONNECT\nuser: %s\npasscode: %s\n\n\x00\n' % (user, passcode)
        self.ss.send(connstr)
        print self.__read(self.ss)
        self.rs.send(connstr)
        print self.__read(self.rs)

        threading.Thread.__init__(self)
        
    def __read(self, sock):
        try:
            while 1:
                c = sock.recv(1024)
                self.buf.append(c)
                if not c or '\x00' in c:
                    break
        except Exception:
            pass
        s = ''.join(self.buf)
        pos = s.find('\x00')
        s1 = s[0:pos]
        s2 = s[pos+1:]
        if len(s2) > 0:
            self.buf = [ s2 ]
        else:
            self.buf = [ ]
        return s1

    def run(self):
        while (self.running and self._parent_thread.isAlive()) \
          or len(self.sendbuf) > 0:
            time.sleep(0.1)
            if len(self.sendbuf) > 0:
                for msg in self.sendbuf:
                    self.rs.sendall(msg)
                self.sendbuf = [ ]
                if not self.running:
                    break
            
            msg = self.__read(self.rs)
            if not msg or msg == '':
                continue
            mat = _destination_re.search(msg)
            if mat:
                dest = mat.group(1)
                for listener in self.listeners:
                    listener.receive(msg)
        print 'connection message loop completed'
        self.ss.close()
        self.rs.close()
        
    # objects listening to subscription messages
    def addlistener(self, listener):
        self.listeners.append(listener)
        
    def dellistener(self, listener):
        self.listeners.remove(listener)
        
    #
    # stomp transmissions
    #
    
    def abort(self, transactionid):
        self.ss.send('ABORT\ntransaction: %s\n\n\x00\n' % transactionid)
    
    def ack(self, messageid, transactionid=None):
        if transactionid:
            header = 'message-id: %s\ntransaction: %s' % (messageid, transactionid)
        else:
            header = 'message-id: %s' % messageid
        self.sendbuf.append('ACK\n%s\n\n\x00\n' % header)
        
    def begin(self, transactionid=None):
        if not transactionid:
            transactionid = _uuid()
        self.ss.send('BEGIN\ntransaction: %s\n\n\x00\n' % transactionid)
        return transactionid
        
    def sendblank(self):
        self.sendbuf.append('\x00\n')
        
    def commit(self, transactionid):
        self.ss.send('COMMIT\ntransaction: %s\n\n\x00\n' % transactionid)
        
    def disconnect(self):
        self.running = None
        self.ss.send('DISCONNECT\n\n\x00\n')
        self.sendbuf.append('DISCONNECT\n\n\x00\n')
        
    def send(self, dest, msg, transactionid=None):
        if transactionid:
            transheader = 'transaction: %s' % transactionid
        else:
            transheader = ''
        self.ss.send('SEND\ndestination: %s\n%s\n\n%s\n\x00\n' % (dest, transheader, msg))
        
    def subscribe(self, dest, ack='auto'):
        self.sendbuf.append('SUBSCRIBE\ndestination: %s\nack: %s\n\n\x00\n' % (dest, ack))

    def unsubscribe(self, dest):
        self.sendbuf.append('UNSUBSCRIBE\ndestination:%s\n\n\x00\n' % dest)
 

#
# command line testing
#
if __name__ == '__main__':

    class StompTester(object):
        def __init__(self, host, port, user='', passcode=''):
            self.c = Connection(host, port, user, passcode)
            self.c.addlistener(self)
            self.c.start()
        
        def receive(self, message):
            print message
            print 'END@'
            
        def ack(self, args):
            if len(args) < 3:
                self.c.ack(args[1])
            else:
                self.c.ack(args[1], args[2])
            
        def abort(self, args):
            self.c.abort(args[1])
            
        def begin(self, args):
            print 'transaction id: %s' % self.c.begin()
            
        def blank(self, args):
            self.c.sendblank()
            
        def commit(self, args):
            if len(args) < 2:
                print 'expecting: commit <transid>'
            else:
                self.c.commit(args[1])
       
        def disconnect(self, args):
            self.c.disconnect()
            
        def send(self, args):
            if len(args) < 3:
                print 'expecting: send <destination> <message>'
            else:
                self.c.send(args[1], ' '.join(args[2:]))
            
        def sendtrans(self, args):
            if len(args) < 3:
                print 'expecting: sendtrans <destination> <transid> <message>'
            else:
                self.c.send(args[1], ' '.join(args[3:]), args[2])
            
        def subscribe(self, args):
            if len(args) < 2:
                print 'expecting: subscribe <destination> [ack]'
            elif len(args) > 2:
                self.c.subscribe(args[1], args[2])
            else:
                self.c.subscribe(args[1])
            
        def unsubscribe(self, args):
            if len(args) < 2:
                print 'expecting: unsubscribe <destination>'
            else:
                self.c.unsubscribe(args[1])

    try:
        if len(sys.argv) < 3:
            print 'USAGE: stomp-test3.py host port [user] [passcode]'
            sys.exit(1)

        host = sys.argv[1]
        port = int(sys.argv[2])
        
        if len(sys.argv) >= 5:
            user = sys.argv[3]
            passcode = sys.argv[4]
        else:
            user = 'test'
            passcode = 'test'
        
        st = StompTester(host, port, user, passcode)
        while 1:
            line = sys.stdin.readline()
            if not line or line.lstrip().rstrip() == '':
                continue
            elif 'quit' in line or 'disconnect' in line:
                st.disconnect(None)
                break
                
            split = line.split()
            if hasattr(st, split[0]):
                getattr(st, split[0])(split)
            else:
                print 'unrecognized command'
    except KeyboardInterrupt:
        st.disconnect(None)

