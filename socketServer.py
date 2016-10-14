'''
    Simple socket server using threads
'''
import socket, time
import sys
from thread import *
from controlThread import *
import model.raspberry as raspModel
 
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    command_q = Queue.Queue()
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
    
    controlThread = WorkerThread(command_q)
    controlThread.daemon = True
    controlThread.start()
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        #Receiving from client
        data = conn.recv(1024)
        data = data.strip()
        print data+"!"
        
        if not data:
            controlThread.join()
            break
        
        if raspModel.strLeft in data and raspModel.strRight in data and raspModel.strTime in data:
            commandDic = makeDicFromStr(data)
            command_q.put(commandDic)
        reply = 'Ok...' + data +'\n'
        conn.send(reply)
    controlThread.park(raspModel.strLeft + raspModel.strRight)
    #came out of loop
    conn.close()
    
# Parse command from client
def makeDicFromStr(instr):
    instr = instr.lower()
    # "left = 1, right =0, time=300" -> "left=1,right=0,time=300"
    instr = instr.replace(" ", "")
    # "left=1,right=0,time=300" -> ["left=1", "right=0", "time=300"]
    instrs = instr.split(",")
    result = {}
    for i in instrs:
        # tmp == ["left", "1"]
        tmp = i.split("=")
        result[tmp[0]] = int(tmp[1])
    return result

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
    
s.close()
