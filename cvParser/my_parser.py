import nltk
import re
import os
from nltk.tag.stanford import NERTagger
from nltk.tokenize import regexp_tokenize
from doc2text import get_docx_text    
import json

##################################################################
##																##
## 							SETUP 								##
## 																##
##################################################################

# Should point to java.exe, requires jre1.8
java_path = "C:\Program Files\Java\jre1.8.0_45\\bin\java.exe" 

# Should point to english.all.3class.distsim.crf.ser.gz and stanford-ner.jar
st = NERTagger(
				'C:/Users/Mungo/Desktop/Python/Projects/cvParser/cvParser/stanford-ner-2014-10-26/classifiers/english.all.3class.distsim.crf.ser.gz', 
				'C:/Users/Mungo/Desktop/Python/Projects/cvParser/cvParser/stanford-ner-2014-10-26/stanford-ner.jar'
				)

##################################################################
##																##
## 							CODE 								##
## 																##
##################################################################

os.environ['JAVAHOME'] = java_path

class MyParser():
	'''A simple .docx CV parser'''
	def __init__(self, file_list, flag):
		self.finalName = ''
		self.finalEmail = ''
		self.DocumentName = ''
		self.keywords = []
		self.file_list = file_list
		self.flag = flag

	def tag_and_tokenize(self,file):
		'''Tokenize, Chuncks and tags string 's' the bulk of the script work (time) is done here'''
		self.text = get_docx_text(file)
		self.sentences = ""
		print("Tokenize and tagging...")
		self.sentences = regexp_tokenize(self.text, pattern='\w+|\$[\d\.]+|\S+')
		self.sentences = [st.tag(self.sentences)]
		print("Tagging done")
	
	def get_name(self):
		'''Currently finds the first name mentioned in the string'''
		self.words = []
		self.name = ''
		self.words_dict = {}
		
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
		self.finalName = ''
		for x in self.n_list:
			for y in x:
				self.finalName += self.words_dict[y][0] + " "

	def get_keywords(self):
		'''Currently identifies keywords mentioned in the CV such as Organisations etc...'''
		self.keywords = []
		for element in self.words_dict:
			if self.words_dict[element][1] != 'PERSON' and self.words_dict[element][1] != 'O':
				self.keywords.append(self.words_dict[element][0])
	
	def get_emails(self):
		"""Returns an iterator of matched emails found in string text."""
		# Removing lines that start with '//' because the regular expression
		# mistakenly matches patterns like 'http://foo@bar.com' as '//foo@bar.com'.
		regex = re.compile(("([a-zA-Z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
	"{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
	"\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

		for email in re.findall(regex, self.text):
			self.finalEmail = email[0] 
	
	def get_results(self, file):
		if self.flag == 0:
			self.tag_and_tokenize(file)
			self.get_name()
			self.get_keywords()
			self.get_emails()
			self.DocumentName = file
		else:
			print("Please close all open documents in the working directory before continuing...")

	def write_json_file(self):
		output_name = input("Output filename (only .txt supported)>:  ")

		if output_name[-4:] != '.txt':
			output_name += '.txt'

		# Line wipes any contents inside output_name.txt
		with open(output_name, 'w') as wipe: 
				wipe.closed

		for f in self.file_list:
			MyParser.get_results(self, f)

			self.results_dict = { 
						'name' : self.finalName,
						'email' : self.finalEmail,
						'document Name' : self.DocumentName,
						'keywords' : self.keywords,
		}

			with open (output_name, 'a') as outfile:
				json.dump(self.results_dict, outfile, sort_keys=True, indent=4, separators=(',', ': '))
				outfile.write('\n')
			outfile.closed