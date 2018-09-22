#!/usr/bin/python -tt

# Author: Md Dalwar Hossain Arif
# Copy Right: Md Dalwar Hossain Arif
# License: Under GPU License
# Restriction: Proprietary information can't be removed
# For more information: www.pysource.org/privacy/
# ---------------------------------------------------------------------------------------------------
# Python Interpreter: 3.4.1
# mySQL Database Version: 5.6.11
# pymysql Version: 0.4
# ---------------------------------------------------------------------------------------------------
# Import Built-In Libraries
import os
import datetime
import shutil
# Define checkFiles() function to detemine whether file exists or not
def checkFiles(rawFileLocation,inputFileLocation,dateSuffix):
	# Introduce source location - (Provide exact file name if possible, or create a function to find the file)
	vendorDirList = [
					# Daily files - convert if necessary
					['PRS','PRS1_'],
					['PRS','PRS2_'],
					['PRS','PRS3_'],
					['NETACT','Netact_'],
					['NETACT_CE','Netact_CE_']
					]
	pathSep = '/'
	# Introduce a file counter to check on total file number
	fileCounter = 0
	# Loop through the list and check for the files -
	print('\nTrying to copy necessary files.\n', end='\n')
	for vendorDir in vendorDirList:
		# Introduce source file's full path with file extension
		srcFolder = rawFileLocation + pathSep + vendorDir[0] + pathSep
		srcFileName = vendorDir[1] + dateSuffix  + '.csv'
		fileSrcPath =  srcFolder + srcFileName
		if os.path.isfile(fileSrcPath) and os.path.exists(fileSrcPath):
			shutil.copy2(fileSrcPath,inputFileLocation)
			print('> {} - {} -> exists -> copied'.format(vendorDir[0], srcFileName), end='\n')
			fileCounter += 1
		else:
			print('* {} - {} -> does not exists'.format(vendorDir[0], srcFileName), end='\n')
			continue
	if fileCounter == len(vendorDirList):
		print('\nAll files exists for - {}'.format(dateSuffix), end='\n')
		return 1
	else:
		print('\nTotal - {} of {} files exists for - {}'.format(fileCounter, len(vendorDirList), dateSuffix), end='\n')
		return 0
# ---------------------------------------------------------------------------------------------------
# This is the standard boilerplate that calls the main() function
if __name__ == '__main__':
	main()