import os
import sys

class FileFinder():
	'''A class to find the required files to pass to the parser'''
	def __init__(self):
		self.file_list = []
		
	def get_files(self):
		'''console commands are dealt with here''' ### functionality to check if the user has added a .docx ending here should probably be made
		if len(sys.argv) < 2:
			print('need sys.argv command')
			
		elif sys.argv[1] == '-a':
			print('All files in the directory will be analysed...please wait...')
			for file in os.listdir(os.getcwd()):
				if file[-5:] == '.docx':
					self.file_list.append(file)
		
		else:
			pass
			
		return self.file_list