import subprocess as sub
import threading as thread

class pianobar(thread.Thread):
    '''Thread class for handling pianobar'''
    def __init__(self):
        thread.Thread.__init__(self)
        
        self.pianobar = None
        self.running = 1
        
        self.stations = {}
        self.station = ""
        self.title = ""
        self.artist = ""
        self.album = ""
        self.time = None
        
        self.start()
        
    def run(self):
        if self.pianobar == None:
            self.pianobar = sub.Popen("pianobar", stdout=sub.PIPE, stdin=sub.PIPE)
        else:
            return False
        
        line = "";
        while self.running:
            char = self.pianobar.stdout.read(1)
            line += char
            
            if char =='\n':
                self.process(line)
                line = ""
                continue
            
            #Check if pianobar is expecting input
            if char == ':':
                if line.find("Email") != -1:
                    self.pianobar.stdin.write("\n")
                    
                if line.find("Password") != -1:
                    self.pianobar.stdin.write("\n")
                    
                if line.find("station") != -1:
                    self.pianobar.stdin.write("0\n")
                    
                if line.find("Error") != -1:
                    print "Got Error\n"
                    self.running = 0
                    print line
                    
            #Get current time
            if char == '#':
                self.time = self.pianobar.stdout.read(15)
                self.time = self.time.strip().split('/')
                line = ""
        #end while    
            
        self.close()
                
    def process(self, line):
        #print [ord(c) for c in line]
        #print line
        
        #Check if this is part of the station list
        if line.startswith('\033[2K\t'):
            num, x, name = line.partition(")")
            num = num[5:].strip()
            name = name[5:]
            self.stations.update({num : name})
            #print num + " " + name
            return
        
        #Check for station change
        if line.find("Station") != -1:
            linesplit = line.split('"',2)
            if len(linesplit) == 3:
                self.station = linesplit[1]
                print "Playing station: " + self.station
            
            #print linesplit
            return
        
        #Must be song change
        if line.find("|>") != -1:
            linesplit = line.split('"',6)
            if len(linesplit) == 7:
                self.title = linesplit[1]
                self.artist = linesplit[3]
                self.album = linesplit[5]
                print "Now playing: " + self.title + " by " + self.artist
            
            return
                
        
        
    def close(self):
        print "Closing pianobar..."
        self.pianobar.stdin.write('q')
        self.pianobar.stdout.close()
        self.pianobar.stdin.close()
        
            
            
            