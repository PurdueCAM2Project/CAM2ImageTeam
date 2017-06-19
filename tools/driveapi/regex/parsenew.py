import re
from os import listdir
from os.path import isfile

""" Parse files with new name format

	This script provides an example for how to parse files
	with the new name format using regex.    

	Last edited: May 18, 2017.  3:20 pm
	Author	   : John Laiman
	Contact    : jlaiman@purdue.edu
"""

name_pattern = re.compile(r"""(\d{4})	  # year
	(\d{2})								  # month
	(\d{2})								  # day
	(\d{2})								  # hour
	(\d{2})								  # minute
	(\d{2})								  # second
	(\d{6})_						      # millisecond
	(\d{1,7})	  						  # cam id
	(.*)$							      # file extension
	""", re.VERBOSE)

for image in listdir('.'):
	img_name = name_pattern.search(image)

	if img_name == None:
		continue

	year   = img_name.group(1)
	month  = img_name.group(2)
	day    = img_name.group(3)
	hour   = img_name.group(4)
	minute = img_name.group(5)
	sec    = img_name.group(6)
	milsec = img_name.group(7)
	cam_id = img_name.group(8)
	filext = img_name.group(9)