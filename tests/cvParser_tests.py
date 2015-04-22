from nose.tools import *
import sys
sys.path.append("C:\Users\Mungo\Desktop\Python\Projects\cvParser\cvParser")
from main import get_files

def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

def test_basic():
	assert