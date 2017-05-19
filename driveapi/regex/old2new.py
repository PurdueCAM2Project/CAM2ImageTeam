import re
from shutil import move
from os import listdir
from os.path import isfile, join, abspath

""" Rename old files with new format
	
	This script allows a user to iteratively (in a folder)
	rename all image files with an old file format so that 
	they use the new file format.  Execute script in folder 
	that contains images to be renamed.  

	Last edited: May 18, 2017.  3:20 pm
	Author	   : John Laiman
	Contact    : jlaiman@purdue.edu
"""


# regex expression used to match old format of image name
name_pattern = re.compile(r"""(\d{1,7}?)_ # cam id
	(\d{4})-							  # year
	(\d{2})-							  # month
	(\d{2})_							  # day
	(\d{2})-							  # hour
	(\d{2})-							  # minute
	(\d{2})-							  # second
	(\d{6})							      # millisecond
	(.*?)$							      # file extension
	""", re.VERBOSE)

for old_name in listdir('.'):
	old_format = name_pattern.search(old_name)

	# If file does not have old file format, loop
	if old_format == None:
		continue

	# Parse information
	cam_id = old_format.group(1)
	year   = old_format.group(2)
	month  = old_format.group(3)
	day    = old_format.group(4)
	hour   = old_format.group(5)
	minute = old_format.group(6)
	sec    = old_format.group(7)
	milsec = old_format.group(8)
	filext = old_format.group(9)

	# Regroup information into new file name format
	new_name = year + month + day + hour + minute + sec + milsec + '_' + cam_id + filext

	# Set absolute file path
	abs_working_dir = abspath('.')
	old_name = join(abs_working_dir, old_name)
	new_name = join(abs_working_dir, new_name)

	# Use shutil.move to rename
	move(old_name, new_name)