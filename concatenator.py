#!/usr/bin/python

import sys, argparse

class Concatenator():
    "Concatenate the entries"
    def __init__(self):
        self.text, self.file, self.destination, self.order = [], [], "", []
        self.flags = [False, False, False, False] # Text, File, Order, Save

        #Parser initialisation
        self.parser = argparse.ArgumentParser(description='Basic concatenation program')

        self.parser.add_argument('-F', action="store", dest="source", help="File(s) to concatenate.", nargs='+')
        self.parser.add_argument('-t', action="store", dest="text", help="Text(s) to concatenate.", nargs='+')
        self.parser.add_argument('-o', action="store", dest="order", help="Set the order. Type 'text' and 'file' in the order you want. By default the texts is after the files.", nargs='+')
        self.parser.add_argument('-s', action="store", dest="destination", help="File to save the output.", nargs=1)

        self.parser.add_argument('--version', action='version', version='%(prog)s 1.0')

        if len(sys.argv)==1:
            self.parser.print_help()
            sys.exit(1)

        args, unknown = self.parser.parse_known_args()

        # Check the arguments
        if unknown:
            self.displayError('Unknown argument(s) : ' + str(unknown).strip('[]') + '\n')

        # Set the flags
        if args.text != None:
            self.text = list(args.text)
            self.flags[0] = True
        if args.source != None:
            self.file = list(args.source)
            self.flags[1] = True
        if args.order != None:
            self.order = list(args.order)
            self.flags[2] = True
        if args.destination != None:
            self.destination = args.destination[0]
            self.flags[3] = True

        self.main()

    def main(self):
        "Main function"
        concatenateText, concatenateList, filesList, tempList = "", [], [], []
        outputLength, filesSize, nbFiles, lineIt = 1, [], len(self.file) + len(self.text), []
        j = 0

        # Check if there is at least two entries to concatenate
        if len(self.text) + len(self.file) < 2:
            self.displayError('At least two entries are required.\n')
        
        # Copy
        for file in self.file:
            tempList[:] = []
            try:
                f = open(file, 'r')
                for line in f:
                    tempList.append(str(line).strip('\n'))
                f.close()
                filesList.append(list(tempList))
            except:
                self.displayError("No such file or directory: " + file + "\n")

        # Add texts to filesList
        for text in self.text:
            tempList[:] = []
            tempList.append(str(text))
            filesList.append(list(tempList))

        print filesList
                
        # Calculation of the length of the lists
        for fileList in filesList:
            filesSize.append(len(fileList))
        for size in filesSize:
            outputLength *= size

        for index in range(nbFiles):
            lineIt.append(self.nbCall(filesSize, index))

        # Initialisation of the output
        for i in range(outputLength):
            concatenateList.append("")

        # Concatenation                   
        for n in range(nbFiles):
            for i in range(outputLength):
                if i%lineIt[n] == 0:
                    concatenateList[i] += filesList[n][j]
                    j += 1
                    if j == filesSize[n]:
                        j = 0
                else:
                    concatenateList[i] += filesList[n][j]

        # Save or display the output
	if self.flags[3]:
            self.saveOutput(concatenateList)
        else:
	    for text in concatenateList:
                print text

    def nbCall(self, filesSize, index):
        if index == 0:
            return 1
        else:
            return filesSize[index-1] * self.nbCall(filesSize, index-1)


    def saveOutput(self, textList_hash):
        myFile = open(self.destination, "w")
        for text in textList_hash:
            myFile.write(str(text))
            myFile.write('\n')
        myFile.close()

    def displayError(self, error):
	print error
	self.parser.print_help()
	sys.exit()	

# Programme de test
if __name__ == "__main__":
    app = Concatenator()
