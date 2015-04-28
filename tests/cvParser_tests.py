from nose.tools import *
import sys
sys.path.append("C:\Users\Mungo\Desktop\Python\Projects\cvParser\cvParser")
from filefinder import FileFinder
from my_parser import MyParser

def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

def test_basic():
	assert