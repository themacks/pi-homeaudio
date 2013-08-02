import subprocess as sub
import threading as thread
import Queue

class pianobar(thread.Thread):
    '''Thread class for handling pianobar'''
    def __init__(self, cmd_q, status_q):
        super(pianobar, self).__init__()
        #thread.Thread.__init__(self)
        
        self.cmd_q = cmd_q              #control command (input)
        self.status_q = status_q        #status updates (output)
        self.stoprequest = thread.Event()
        
        self.pianobar = None
        
        self.stations = {}
        self.station = ""
        self.title = ""
        self.artist = ""
        self.album = ""
        self.time = None
        
        self.start()
        
    def run(self):
        print("Starting Pianobar...")
        self.pianobar = sub.Popen("pianobar", stdout=sub.PIPE, stdin=sub.PIPE)
        
        line = "";
        while not self.stoprequest.isSet():
            #try reading a command from the queue
            try:
                command = self.cmd_q.get_nowait()
                print "Received command"
                
                #process the command
                print command
            #on empty queue check for pianobar output
            except Queue.Empty:        
                char = self.pianobar.stdout.read(1)
                line += char
            
                if char =='\n':
                    self.process(line)
                    line = ""
                    continue
            
                #Check if pianobar is expecting input
                if char == ':':
                    if line.find("Email") != -1:
                        #self.pianobar.stdin.write("\n")
                        print("Requesting username...")
                        self.status_q.put({ "type" : "get",
                                            "get"  : "user"})
                    
                    if line.find("Password") != -1:
                        #self.pianobar.stdin.write("\n")
                        print("Requesting password...")
                        self.status_q.put({ "type" : "get",
                                            "get"  : "password"})
                    
                    if line.find("station") != -1:
                        self.pianobar.stdin.write("0\n")
                        self.status_q.put({ "type" : "get",
                                            "get"  : "station"})
                    
                    if line.find("Error") != -1:
                        print "Got Error\n"
                        self.stoprequest.set()
                        print line
                    
                #Get current time
                if char == '#':
                    self.time = self.pianobar.stdout.read(15)
                    self.time = self.time.strip().split('/')
                    self.status_q.put({ "type" : "time", 
                                        "time" : self.time})
                    line = ""
            #end except
        #end while    
            
        self.close()
    
    def join(self, timeout=None):
        self.stoprequest.set()
        super(pianobar, self).join(timeout)
                
    def process(self, line):
        #print [ord(c) for c in line]
        #print line
        
        #Check if this is part of the station list
        if line.startswith('\033[2K\t'):
            num, x, name = line.partition(")")
            num = num[5:].strip()
            name = name[5:]
            self.stations.update({num : name})
            print "Adding station: " + num + " " + name
            self.status_q.put({ "type"     : "stations", 
                                "stations" : self.stations})
            return
        
        #Check for station change
        if line.find("Station") != -1:
            linesplit = line.split('"',2)
            if len(linesplit) == 3:
                self.station = linesplit[1]
                print "Playing station: " + self.station
                self.status_q.put({ "type"    : "station", 
                                    "station" : self.station})
            return
        
        #Must be song change
        if line.find("|>") != -1:
            linesplit = line.split('"',6)
            if len(linesplit) == 7:
                self.title = linesplit[1]
                self.artist = linesplit[3]
                self.album = linesplit[5]
                print "Now playing: " + self.title + " by " + self.artist
                self.status_q.put({ "type"   : "song", 
                                    "title"  : self.title,
                                    "artist" : self.artist,
                                    "album"  : self.album})
            return
        
    def close(self):
        print "Closing pianobar..."
        self.pianobar.stdin.write('q')
        self.pianobar.stdout.close()
        self.pianobar.stdin.close()

            