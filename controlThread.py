import os, time
import threading, Queue
import model.raspberry as raspModel

class WorkerThread(threading.Thread):
    """ A worker thread that takes directory names from a queue, finds all
        files in them recursively and reports the result.

        Input is done by placing directory names (as strings) into the
        Queue passed in command_q.

        Output is done by placing tuples into the Queue passed in result_q.
        Each tuple is (thread name, dirname, [list of files]).

        Ask the thread to stop by calling its join() method.
    """
    def __init__(self, command_q):
        super(WorkerThread, self).__init__()
        self.command_q = command_q
        self.stoprequest = threading.Event()
        self.latestTime = 0
        self.latestLeft = 0
        self.latestRight = 0
        
    def run(self):
        raspModel.GPIO.setmode(raspModel.GPIO.BOARD)
        raspModel.GPIO.setwarnings(False)
        self.setup()
        
        # As long as we weren't asked to stop, try to take new tasks from the
        # queue. The tasks are taken with a blocking 'get', so no CPU
        # cycles are wasted while waiting.
        # Also, 'get' is given a timeout, so stoprequest is always checked,
        # even if there's nothing in the queue.
        
        while not self.stoprequest.isSet():
            try:
                self.currentTime = int(round(time.time() * 1000))
##                print "currentTime - latestTime :: " + str(self.currentTime - self.latestTime)
                
                if (self.currentTime - self.latestTime) < 300:
                    self.setup()
                    self.move(self.latestLeft, self.latestRight)
                else :
                    self.park(raspModel.strLeft + raspModel.strRight)
                    self.latestLeft = 0
                    self.latestRight = 0
                    
                command = self.command_q.get(True, 0.001)
                                
                self.latestLeft = command[raspModel.strLeft]
                self.latestRight = command[raspModel.strRight]
                self.latestTime = int(round(time.time() * 1000))
                    
            except Queue.Empty:
                continue

    def join(self, timeout=None):
        self.park(raspModel.strLeft+raspModel.strRight)
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)
        
    def setup(self):
        # GPIO setup
        for leftRight in range(2):
            for idx in range(3):
                raspModel.GPIO.setup(raspModel.pinList[leftRight][idx], raspModel.GPIO.OUT)
    
    def move(self, left, right):
        # GPIO output set
        if left == 1:
            self.forward(raspModel.strLeft)
        elif left == 0:
            self.park(raspModel.strLeft)
        elif left == -1:
            self.reverse(raspModel.strLeft)
        if right == 1:
            self.forward(raspModel.strRight)
        elif right == 0:
            self.park(raspModel.strRight)
        elif right == -1:
            self.reverse(raspModel.strRight)

    def park(self, target):
        # GPIO output set
        if raspModel.strLeft in target:
            for idx in range(3):
                raspModel.GPIO.output(raspModel.leftPinList[idx], raspModel.parkOutput[idx])
        if raspModel.strRight in target:
            for idx in range(3):
                raspModel.GPIO.output(raspModel.rightPinList[idx], raspModel.parkOutput[idx])
    def forward(self, target):
        # GPIO output set
        if raspModel.strLeft in target:
            for idx in range(3):
                raspModel.GPIO.output(raspModel.leftPinList[idx], raspModel.forwardOutput[idx])
        if raspModel.strRight in target:
            for idx in range(3):
                raspModel.GPIO.output(raspModel.rightPinList[idx], raspModel.forwardOutput[idx])
    def reverse(self, target):
        # GPIO output set
        if raspModel.strLeft in target:
            for idx in range(3):
                raspModel.GPIO.output(raspModel.leftPinList[idx], raspModel.reverseOutput[idx])
        if raspModel.strRight in target:
            for idx in range(3):
                raspModel.GPIO.output(raspModel.rightPinList[idx], raspModel.reverseOutput[idx])
        
            
        
