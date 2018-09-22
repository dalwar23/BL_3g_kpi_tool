#!/usr/bin/python -tt

# Author: Md Dalwar Hossain Arif
# Copy Right: Md Dalwar Hossain Arif
# License: Under GPU License
# Restriction: Proprietary information can't be removed
# For more information: www.pySource.org
# ---------------------------------------------------------------------------------------------------
# Python Interpreter: 3.4.1
# mySQL Database Version: 5.6.11
# pymysql Version: 0.4
# ---------------------------------------------------------------------------------------------------
# Import Built-In Libraries
import os
import csv
import shutil
import xlrd
from datetime import datetime, date, time, timedelta
import time
# Import custom library functions [these were supposed to be classes but i wrote them in functions]
import ftpOperations
# ---------------------------------------------------------------------------------------------------
# Define a class for the log - it will suppress any warning!!
class CreateLog(object):
	def write(self,text):
		if not text.startswith("WARNING *** OLE2"):
			sys.stdout.write(text)
# ---------------------------------------------------------------------------------------------------
# Define a function to convert to CSV 
def convert2CSV(srcFile, dstFile):
	try:
		# Create a information/warning/Error log -
		log = CreateLog()
		# Open workbook to read -
		workBook = xlrd.open_workbook(srcFile, logfile=log)
		workSheet = workBook.sheet_by_index(0)
		# Open CSV file to write on - 
		csvFile = open(dstFile,'w',newline='')
		writeFile = csv.writer(csvFile, dialect='excel')
		# Create the CSV file
		for rows in range(workSheet.nrows):
			writeFile.writerow(workSheet.row_values(rows))
		# Close the CSV file
		csvFile.close()
		# Convertion to CSV has been done
		print('[ {} ] converted to [ {} ] and saved.'.format(srcFile,dstFile), end='\n')
	except IOError as err:
		print('IO Error!', err, end='\n', sep='->')
	except SameFileError as sferr:
		print('Source and destination are same.', sferr, end='\n', sep='->')
# ---------------------------------------------------------------------------------------------------
# Define a main() function
def main():
	# Download required files
	vendorList = ['Huawei', 'Nokia']
	for item in vendorList:
		downloadStatus = ftpOperations.download(item)
	# Now convert and move files
	dirBase = 'E:/3G_KPI/'
	print('\n> Trying to rename and move required files to specific directory.\n', end='\n')
	# Walk through directory
	for item in vendorList:
		if item == 'Huawei':
			srcDir = dirBase + 'PRS_RAW/'
			hFiles = next(os.walk(srcDir))[2]
			for hFile in hFiles:
				newFileName = hFile[0:13] + hFile[23:]
				# Re-name, Move files and Delete input files
				try:
					srcFile = srcDir + hFile
					dstFile = dirBase + 'PRS/' + newFileName
					shutil.copyfile(srcFile,dstFile,follow_symlinks=True)
					print('[ {} ] -> [ {} ] file moved and saved.'.format(hFile, newFileName), end='\n')
					try:
						os.remove(srcFile)
						print('Inputfile [ {} ] deleted.'.format(hFile),end='\n')
					except OSError:
						print('Error: {} - {}.'.format(hFile,strerror),end='\n')
				except:
					print('Can not move [ {} ] -> [ {} ] file.'. format(item, hFile), end='\n')
		if item == 'Nokia':
			srcDir = dirBase + 'NETACT_RAW/'
			nFiles = next(os.walk(srcDir))[2]
			for nFile in nFiles:
				if '_CE_' in nFile:
					customDate = (date.today()-timedelta(1)).strftime('%Y%m%d')
					newFileName = 'Netact_CE_'+ customDate + '.csv'
					srcFile = srcDir + nFile
					dstFile = dirBase + 'NETACT_CE/' + newFileName
					convert2CSV(srcFile, dstFile)
				if '_KPI_' in nFile:
					customDate = (date.today()-timedelta(1)).strftime('%Y%m%d')
					newFileName = 'Netact_'+ customDate + '.csv'
					srcFile = srcDir + nFile
					dstFile = dirBase + 'NETACT/' + newFileName
					# It's a ';' seperated csv file so need to be converted into ',' separted
					# Open CSV file and write the result
					FILE = open(dstFile,'w', newline='')
					output = csv.writer(FILE, delimiter=',')
					with open(srcFile, 'r') as csvFile:
						reader = csv.reader(csvFile, delimiter=';')
						# Create comma separated CSV
						for row in reader:
							output.writerow(row)
					print('[ {} ] -> [ {} ] file converted and saved.'.format(nFile, newFileName), end='\n')
				try:
					os.remove(srcFile)
					print('Inputfile [ {} ] deleted.'.format(nFile),end='\n')
				except OSError:
					print('Error: {} - {}.'.format(nFile,strerror),end='\n')
# ---------------------------------------------------------------------------------------------------
# This is THE standard boilerplate that calls THE main() function
if __name__ == '__main__':
	main()