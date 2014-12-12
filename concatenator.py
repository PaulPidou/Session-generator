#!/usr/bin/python

import sys, argparse

class Concatenator():
    "Concateante the files in input"
    def __init__(self):
        self.destination = []

        #Parser initialisation
        self.parser = argparse.ArgumentParser(description='Basic concatenation program')

        self.parser.add_argument('-F', action="store", dest="source", help="Input file")
