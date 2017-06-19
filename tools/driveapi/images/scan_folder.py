from os import listdir
from os.path import isfile, join, abspath

pwd = abspath('.')

for file in listdir('.'):
	if file.lower().endswith(('.png','.jpg','.jpeg')):
		# add to image list

	if file.lower().endswith('.xml'):
		# add to label list
