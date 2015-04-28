import os
import sys

class FileFinder():
	'''A class to find the required files to pass to the parser'''
	def __init__(self):
		self.file_list = []
		self.flag = 0
		
	def get_files(self):
		'''console commands are dealt with here''' ### functionality to check if the user has added a .docx ending here should probably be made
		if len(sys.argv) < 2:
			print('need sys.argv command')
			
		elif sys.argv[1] == '-a':
			print('All files in the working directory will be analysed...please wait...')
			for file in os.listdir(os.getcwd()):
				if file[-5:] == '.docx' and file[0:2] != '~$':
					self.file_list.append(file)
				elif file[0:2] == '~$': # test to find out if there are open files currently
					self.flag = 1
		else:
			pass
		
		return self.file_list, self.flag