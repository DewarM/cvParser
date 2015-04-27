######################
######################

### To Add:
### - Telephone number search
### - import pdf
### - output resulting data to json or similar
### - add functionality to run the script in a different folder

from filefinder import FileFinder
from my_parser import MyParser

files = FileFinder()
list_of_files = files.get_files()
parsed_files = MyParser(list_of_files)
parsed_files.get_results()