######################
######################

### To Add:
### - Telephone number search
### - import pdf
### - output resulting data to json or similar
### - add functionality to run the script in a different folder

from doc2text import get_docx_text
import nltk
import os
import json
import urllib
from workfile import data
import re
import sys

from nltk.tag.stanford import NERTagger
java_path = "C:\Program Files\Java\jre1.8.0_45\\bin\java.exe"
os.environ['JAVAHOME'] = java_path
### For future the string used to find the tagger should be custom on setup
st = NERTagger('C:/Users/Mungo/Desktop/Python/Projects/cvParser/cvParser/stanford-ner-2014-10-26/classifiers/english.all.3class.distsim.crf.ser.gz', 'C:/Users/Mungo/Desktop/Python/Projects/cvParser/cvParser/stanford-ner-2014-10-26/stanford-ner.jar')

class FileFinder():
	'''A class to find the required files to pass to the parser'''
	def __init__(self):
		pass
		
	def get_files(self):
		'''console commands are dealt with here''' ### functionality to check if the user has added a .docx ending here should probably be made
		if len(sys.argv) < 2:
			print('need sys.argv command')
			
		elif sys.argv[1] == '-a':
			print('All files in the directory will be analysed')
			print([f for f in os.listdir(os.getcwd()) if f[-5:] == '.docx'])
			for file in os.listdir(os.getcwd()):
				if file[-5:] == '.docx':
					y = MyParser(file)
					y.results()

class MyParser():
	'''A simple docx CV parser'''
	def __init__(self, document):
		self.finalName = ''
		self.finalEmail = ''
		self.DocumentName = document
		self.text = get_docx_text(document)
		
	
	def tag_and_tokenize(self):
		'''Tokenize, Chuncks and tags string 's' the bulk of the script work (time) is done here'''
		self.sentences = nltk.sent_tokenize(self.text)
		self.sentences = [nltk.word_tokenize(self.sent) for self.sent in self.sentences]
		self.sentences = [st.tag(self.sent) for self.sent in self.sentences]
		print("tagging done")
	
	def get_name(self):
		'''Currently finds the first name mentioned in the string'''
		self.words = []
		self.name = ''
	
		for x in self.sentences:
			for y in x:
				for z in y:
					self.words.append(z)	

		self.numbered = range(0, len(self.words))
		self.words_dict = dict(zip(self.numbered, self.words))
		self.n_list = []
		self.n = 1
		
		for element in self.words_dict:
			element_next = element + self.n	
			if self.words_dict[element][1] == 'PERSON' and len(self.n_list) < 1:
				while self.words_dict[element_next][1] == 'PERSON':
					element_next = element + self.n
					self.n += 1
				self.n_list.append(list(range(element, element + self.n - 1)))
			elif len(self.n_list) > 1:
				break
		for x in self.n_list:
			for y in x:
				self.finalName += self.words_dict[y][0] + " "
	
	def get_emails(self):
		"""Returns an iterator of matched emails found in string text."""
		# Removing lines that start with '//' because the regular expression
		# mistakenly matches patterns like 'http://foo@bar.com' as '//foo@bar.com'.
		regex = re.compile(("([a-zA-Z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
	"{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
	"\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

		for email in re.findall(regex, self.text):
			self.finalEmail = email[0] 
	
	def results(self):
		self.tag_and_tokenize()
		self.get_name()
		self.get_emails()
		print('Document Name: ', self.DocumentName)
		print('Name: ', self.finalName)
		print('Email: ', self.finalEmail)
		


start = FileFinder()
start.get_files()	
