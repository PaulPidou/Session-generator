#!/usr/bin/python

import sys, argparse
import time, datetime
import base64, hashlib

class Application():
    "Basic session generator"
    def __init__(self):
        # Variables initialisation
	self.flags = [False, False, False, False, False, False, False] # Time, Text, Duration, Encoding, Concatenate, Order, Save 
	self.supportEncoding = ['base64', 'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'all']
        self.time, self.text, self.duration, self.encoding, self.order, self.destination = [], [], 0, [], [], ""

        #Parser initialisation
        self.parser = argparse.ArgumentParser(description='Basic session generator')

        self.parser.add_argument('-T', action="store", dest="time", help="Time(s) to encode, format -> d/m/y h:min:s Or type 'current' to use the current time", nargs='+')
        self.parser.add_argument('-t', action="store", dest="text", help="Text(s) to encode", nargs='+')
        self.parser.add_argument('-d', action="store", dest="duration", help="Duration after the start time in minutes.", type=int, nargs=1)
        self.parser.add_argument('-e', action="store", dest="encoding", help="Enconding wished. Currently support : 'base64', 'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'. Type 'all' to use them all this order. By default : None", nargs='+')
        self.parser.add_argument('-c', action="store_true", default=False, dest="concatenate", help="Set the contenation to true.") 
        self.parser.add_argument('-o', action='store', dest="order", help="Set the order for the concatenation when you use time and text together. Type 'text' and 'time' in the order you want to concatenate them.", nargs="+")
        self.parser.add_argument('-s', action="store", dest="destination", help="File to save the output", nargs=1)

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
	if args.order != None:
            self.order = list(args.order)
            self.flags[5] = True
        if args.destination != None:
            self.destination = args.destination
	    self.flags[6] = True

	self.flags[4] = args.concatenate
        
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

	# Text without encoding
	elif self.flags[1] and not self.flags[3]:
	    self.displayError("Please select an encoding or type '-e all'\n")

	# Duration without time
	elif self.flags[2]:
	    self.displayError("You need to type a datetime. Type '-T current' to use the current time.\n")

        # Check the contenation 
	if self.flags[5] and not self.flags[4]:
            self.displayError("You have to activate the concatenation before setting an order.\n")

        if self.flags[5] and not self.flags[0] or not self.flags[1]:
            self.displayError("You must use text and time together to set an order.\n")

        if self.flags[5]:
            if len(self.order) != self.order.count('time') + self.order.count('text'):
                self.displayError("Type only 'time' and 'text' to set the order.\n")
            elif len(self.order) != len(self.text) + len(self.time):
                self.displayError("You have to type as many position chains as input.\n")
            elif len(self.text) != self.order.count('text') or len(self.time) != self.order.count('time'):
                self.displayError("You have to type as many 'text' in the order as text input and as many 'time' in the order as time input.\n")

	# Text without time
	elif self.flags[1] and not self.flags[0]:
	    if len(self.encoding) != 1 and len(self.encoding) != len(self.text):
		if len(self.text) != 1:
		    self.displayError('You must choose one encoding for all strings or one encoding for each string\n')
	    if len(self.encoding) == 1: 
	        for text in self.text:
		    textList_hash.append(self.encoder(text, self.encoding[0]))
	    else:
		if len(self.text) != 1: # len(text) == len(encoding)
		    for index, text in enumerate(self.text):
		        textList_hash.append(self.encoder(text, self.encoding[index]))
		else: # len(text) == 1
		    for index, code in enumerate(self.encoding):
			textList_hash.append(self.encoder(self.text[0], code))

	# Date with encoding and without text
	if self.flags[0] and self.flags[3] and not self.flags[1]:
	    if len(self.encoding) != 1 and len(self.encoding) != len(self.time):
		if len(self.time) != 1:
		    self.displayError('You must choose one encoding for all dates or one encoding for each date\n')
	    if not self.flags[2]:
	        if len(self.encoding) == 1: 
	            for time in timeList_start:
		        textList_hash.append(self.encoder(time, self.encoding[0]))
	        else:
		    if len(self.time) != 1: # len(time) == len(encoding)
		        for index, time in enumerate(timeList_start):
		            textList_hash.append(self.encoder(time, self.encoding[index]))
		    else: # len(time) == 1
		        for index, code in enumerate(self.encoding):
			    textList_hash.append(self.encoder(timeList_start[0], code))
	    else:
		if len(self.encoding) == 1: 
	            for timeList in timeList_duration:
			for time in timeList:
		            textList_hash.append(self.encoder(time, self.encoding[0]))
	        else:
		    if len(self.time) != 1: # len(time) == len(encoding)
		        for index, timeList in enumerate(timeList_duration):
			    for time in timeList:
		                textList_hash.append(self.encoder(time, self.encoding[index]))
		    else: # len(time) == 1
			for time in timeList_duration[0]:
			    for code in self.encoding:
		                textList_hash.append(self.encoder(time, code))

        # Date with text

	print textList_hash
	    
	
	
        #listGen = self.encoder()
        
	# Save or display the output
	#if self.flags[4]:
            #self.saveOutput(listGen)
        #else:
	    #for gen in listGen:
                #print gen	

    def encoder(self, text, method):           
        encodedList = []

        if method == 'base64' or method == 'all':
	    encodedList.append(base64.b64encode(str(text))[:-2])

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

    def saveOutput(self, listGen):
        myFile = open(self.destination, "w")
        for gen in listGen:
            myFile.write(str(gen))
            myFile.write('\n')
        myFile.close()

    def displayError(self, error):
	print error
	self.parser.print_help()
	sys.exit()	

# Programme de test
if __name__ == "__main__":
    app = Application()
