#!/usr/bin/python

import sys, argparse
import time, datetime
import base64, hashlib

class SessionGenerator():
    "Basic session generator"
    def __init__(self):
        # Variables initialisation
	self.flags = [False, False, False, False, False, False, False] # Time, Text, Duration, Cookie-friendly, Encoding, Save, File 
	self.supportEncoding = ['base64', 'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'all']
        self.time, self.text, self.duration, self.encoding, self.destination, self.file = [], [], 0, [], "", []

        #Parser initialisation
        self.parser = argparse.ArgumentParser(description='Basic session generator')

        self.parser.add_argument('-F', action="store", dest="file", help="File(s) to encode.", nargs='+') 
        self.parser.add_argument('-t', action="store", dest="text", help="Text(s) to encode", nargs='+')
        self.parser.add_argument('-T', action="store", dest="time", help="Time(s) to encode, format -> d/m/y h:min:s Or type 'current' to use the current time", nargs='+')
        self.parser.add_argument('-d', action="store", dest="duration", help="Duration after the start time in minutes.", type=int, nargs=1)
        self.parser.add_argument('-e', action="store", dest="encoding", help="Enconding wished. Currently support : 'base64', 'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'. Type 'all' to use them all this order. By default : None", nargs='+')
        self.parser.add_argument('-cf', action="store_true", default=False, dest="cookie_friendly", help="The output will be cookie friendly.") 
        self.parser.add_argument('-s', action="store", dest="destination", help="File to save the output", nargs=1)

        self.parser.add_argument('--version', action='version', version='%(prog)s 1.0')

        if len(sys.argv)==1:
            self.parser.print_help()
            sys.exit(1)

        args, unknown = self.parser.parse_known_args()

        # Check the arguments
        if unknown:
            self.displayError('Unknown argument(s) : ' + str(unknown).strip('[]') + '\n')
        
	# Set the flags
        if args.time != None:
            self.time = list(args.time)
	    self.flags[0] = True
	if args.text !=None:
	    self.text = list(args.text)
	    self.flags[1] = True
        if args.duration != None:
            self.duration = args.duration[0]
	    self.flags[2] = True
        if args.encoding != None:
            self.encoding = list(args.encoding)
	    self.flags[3] = True
        if args.destination != None:
            self.destination = args.destination[0]
	    self.flags[5] = True
	if args.file != None:
            self.file = list(args.file)
            self.flags[6] = True

	self.flags[4] = args.cookie_friendly
        
        self.main()

    def main(self):
	"Main function"
	timeList_start = [] # List of timestamp (from the input)
	timeList_duration = [] # List of timestamp (from the input with duration)
	textList_hash = [] # List of hash

	# Date
	if self.flags[0]:
	    # Remplace 'currrent' by a formatted date
            self.processTime()
	    # Get the timestamp for each date
	    for time in self.time:
		timeList_start.append(self.getTimeInt(time))

	    if self.flags[2]: # Duration
		if self.duration < 1:
		    self.displayError('The duration must be at least 1 minute\n')
		for time in timeList_start:
		    timeList_duration.append(self.getTimeDuration(time))

	    if self.flags[3]: # Encoding
                if timeList_duration:
                    for time in timeList_duration:
                        for code in self.encoding:
                            textList_hash.append(self.encoder(time, code))
                else:
                    for time in timeList_start:
                        for code in self.encoding:
                            textList_hash.append(self.encoder(time, code))

	# Text without encoding or file without encoding
	elif (self.flags[1] or self.flags[6]) and not self.flags[3]:
	    self.displayError("Please select an encoding or type '-e all'\n")

	# Duration without time
	elif self.flags[2]:
	    self.displayError("You need to type a datetime. Type '-T current' to use the current time.\n")

	# Text
	if self.flags[1]:
            for text in self.text:
                for code in self.encoding:
                    textList_hash.append(self.encoder(text, code))

        # File
        if self.flags[6]:
            for file in self.file:
                try:
                    f = open(file, 'r')
                    for line in f:
                        for code in self.encoding:
                            textList_hash.append(self.encoder(line, code))
                    f.close()
                except:
                    self.displayError("No such file or directory: " + file + "\n")
        
	# Save or display the output
	if self.flags[5]:
            self.saveOutput(textList_hash)
        else:
	    for textList in textList_hash:
                for text in textList:
                    print text	

    def encoder(self, text, method):           
        encodedList = []

        if method == 'base64' or method == 'all':
            if self.flags[4]: # Cookie friendly
                encodedList.append(base64.b64encode(str(text)).strip('='))
            else:
                encodedList.append(base64.b64encode(str(text)))

        if method == 'md5' or method == 'all':
            hashMd5 = hashlib.md5(str(text).encode())
            encodedList.append(hashMd5.hexdigest())

        if method == 'sha1' or method == 'all':
            hashSha1 = hashlib.sha1(str(text).encode())
            encodedList.append(hashSha1.hexdigest())

        if method == 'sha224' or method == 'all':
            hashSha224 = hashlib.sha224(str(text).encode())
            encodedList.append(hashSha224.hexdigest())

        if method == 'sha256'or method == 'all':
            hashSha256 = hashlib.sha256(str(text).encode())
            encodedList.append(hashSha256.hexdigest())

        if method == 'sha384' or method == 'all':
            hashSha384 = hashlib.sha384(str(text).encode())
            encodedList.append(hashSha384.hexdigest())

        if 'sha512' in self.encoding or 'all' in self.encoding:
            hashSha512 = hashlib.sha512(str(text).encode())
            encodedList.append(hashSha512.hexdigest())      

        if not method in self.supportEncoding:
            self.displayError('Wrong encoding\n')

        return encodedList

    def processTime(self):
	"Remplace 'currrent' by a formatted date"
	while 'current' in self.time:
	    index = self.time.index("current")
	    self.time[index] = self.getCurrentTimeString()

    def getCurrentTimeString(self):
	return time.strftime("%d/%m/%Y %H:%M:%S")

    def getTimeInt(self, formattedTime):
	try:
	    return int(time.mktime(datetime.datetime.strptime(formattedTime, "%d/%m/%Y %H:%M:%S").timetuple())) 
        except :
            self.displayError('The time format is not valid\n')

    def getTimeDuration(self, timestamp):
	timeList, duration, i = [], self.duration*60, 0
	while i < duration:
	    timeList.append(timestamp)
	    timestamp += 1
	    i += 1
	return timeList    

    def saveOutput(self, textList_hash):
        myFile = open(self.destination, "w")
        for textList in textList_hash:
            for text in textList:
                myFile.write(str(text))
                myFile.write('\n')
        myFile.close()

    def displayError(self, error):
	print error
	self.parser.print_help()
	sys.exit()	

# Programme de test
if __name__ == "__main__":
    app = SessionGenerator()
