#!/usr/bin/python

import sys, argparse
import time, datetime
import base64, hashlib

class Application():
    "Basic session generator"
    def __init__(self):
        self.time, self.duration,self.encoding, self.destination = "", 5, "", ""
        self.parser = argparse.ArgumentParser(description='Basic session generator')

	self.parser.add_argument('-t', action="store", dest="time", help="Start time, format -> d/m/y h:min:s If the time is not specify the current time is taken")
	self.parser.add_argument('-d', action="store", dest="duration", help="Duration after the start time in minutes By default : 5 mins", type=int)
	self.parser.add_argument('-e', action="store", dest="encoding", help="Enconding wished. Currently support : 'md5', 'base64', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'. By default : None")
	self.parser.add_argument('-s', action="store", dest="destination", help="File used to save the output")

	args, unknown = self.parser.parse_known_args()

        # Check the arguments
	if unknown:
	    print 'Unknown argument(s) : ' + str(unknown).strip('[]') + '\n'
	    self.parser.print_help()
	    sys.exit()
	
	if args.time != None:
	    self.time = args.time
	if args.duration != None:
	    self.duration = args.duration
	if args.destination != None:
	    self.destination = args.destination

	if self.duration < 1:
            print 'Duration must be at least 1 min\n'
            self.parser.print_help()
            sys.exit()

	self.encoding = args.encoding
	
	self.main()

    def main(self):
	if self.time == "":
	    self.setTime()

	listGen = self.generator()
	if self.destination == "":
	    print listGen
	else:
	    self.saveOutput(listGen)

    def generator(self):
	try:
	    timestamp = int(time.mktime(datetime.datetime.strptime(self.time, "%d/%m/%Y %H:%M:%S").timetuple()))
	except :
	    print 'The time format is not valid\n'
	    self.parser.print_help()
	    sys.exit()
	    
	timeList, encodedList, i, duration = [], [], 0, self.duration*60
	while i < duration:
	    timestamp += 1
	    timeList.append(timestamp)
	    i += 1

	if self.encoding == None:
	    return timeList

	elif self.encoding == 'md5':
	    for ts in timeList:
		hashMd5 = hashlib.md5(str(ts).encode())
		encodedList.append(hashMd5.hexdigest())
	
	elif self.encoding == 'base64':
	    for ts in timeList:
		encodedList.append(base64.b64encode(str(ts))[:-2])

	elif self.encoding == 'sha1':
	    for ts in timeList:
		hashSha1 = hashlib.sha1(str(ts).encode())
		encodedList.append(hashSha1.hexdigest())

	elif self.encoding == 'sha224':
	    for ts in timeList:
		hashSha224 = hashlib.sha224(str(ts).encode())
		encodedList.append(hashSha224.hexdigest())

	elif self.encoding == 'sha256':
	    for ts in timeList:
		hashSha256 = hashlib.sha256(str(ts).encode())
		encodedList.append(hashSha256.hexdigest())

	elif self.encoding == 'sha384':
	    for ts in timeList:
		hashSha384 = hashlib.sha384(str(ts).encode())
		encodedList.append(hashSha384.hexdigest())

	elif self.encoding == 'sha512':
	    for ts in timeList:
		hashSha512 = hashlib.sha512(str(ts).encode())
		encodedList.append(hashSha512.hexdigest())		

	else:
	    print 'Wrong encoding\n'
	    print self.parser.print_help()
	    sys.exit()

	return encodedList

    def setTime(self):
	now = datetime.datetime.now()
	self.time = str(now.day) + '/' + str(now.month) + '/' + str(now.year) + ' ' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second)

    def saveOutput(self, listGen):
	myFile = open(self.destination, "w")
	for gen in listGen:
	    myFile.write(str(gen))
	    myFile.write('\n')
	myFile.close()

# Programme de test
if __name__ == "__main__":
    app = Application()
