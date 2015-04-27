from doc2text import get_docx_text
import nltk
import re
from nltk.tag.stanford import NERTagger
import os

from nltk.tokenize import regexp_tokenize
    

java_path = "C:\Program Files\Java\jre1.8.0_45\\bin\java.exe" ### Java path may need to be changed, note jre.8 is required for the stanford tagger
os.environ['JAVAHOME'] = java_path
### For future the string used to find the tagger should be custom on setup
st = NERTagger('C:/Users/Mungo/Desktop/Python/Projects/cvParser/cvParser/stanford-ner-2014-10-26/classifiers/english.all.3class.distsim.crf.ser.gz', 'C:/Users/Mungo/Desktop/Python/Projects/cvParser/cvParser/stanford-ner-2014-10-26/stanford-ner.jar')



class MyParser():
	'''A simple .docx CV parser'''
	def __init__(self, file_list):
		self.finalName = ''
		self.finalEmail = ''
		self.file_list = file_list
		
	
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
		self.finalName = ""
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
	
	def get_results(self):
		for self.file in self.file_list:
			self.tag_and_tokenize(self.file)
			self.get_name()
			self.get_emails()
			self.DocumentName = self.file
			print('Document Name: ', self.DocumentName)
			print('Name: ', self.finalName)
			print('Email: ', self.finalEmail)