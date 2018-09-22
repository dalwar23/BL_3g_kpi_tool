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
from datetime import datetime, date, time, timedelta
import time
import ftplib
# Define a function to connect to FTP server
def ftpConnect(ftpHost,ftpUserName,ftpPassword):
	# Connect to FTP server
	try:
		ftp = ftplib.FTP(ftpHost,ftpUserName,ftpPassword)
		if ftp:
			print('\n> Connected and logged into [ {} ] FTP server.\n'.format(ftpHost), end='\n')
	except:
		print('Could not log in to [ {} ] FTP server.'.format(ftpHost), end='\n\n')
	return ftp
# Define a function to execute download operation
def downloadFiles(flag, ftp,rDir,lDirBase, customDate):
	# Get required files' list and download
	cWD = ftp.cwd(rDir)
	# Intorduce a blank list to list file names
	remoteFileList = []
	dFileList = []
	# Now append all the file names to the previously created empty list
	ftp.retrlines('NLST',callback=remoteFileList.append)
	# Now Print all the file names
	for file_ in remoteFileList:
		if flag == 'Huawei' and (customDate in file_):
			lDir = lDirBase + 'PRS_RAW/'
			dFileList.append(file_)
		if flag == 'Nokia' and customDate in file_ and ('_CE_' in file_ or '_KPI_' in file_):
			dFileList.append(file_)
			lDir = lDirBase + 'NETACT_RAW/'
	for dFile in dFileList:
		# Download file
		fileSize_ = ftp.size(dFile)
		fileSizeMB = fileSize_/(1024*1024)
		localFile = os.path.join(lDir,dFile)
		fileName = open(localFile,'wb')
		download = ftp.retrbinary('RETR ' + dFile, fileName.write)
		if download:
			print('[ {} ] - [ {:.3f} MB ] has been downloaded to [ {} ]'.format(dFile, fileSizeMB, lDir), sep=' ', end='\n')
		else:
			print ('Download ERROR!')
		fileName.close()
	ftp.close()	
# Define a function for downloading files/folders
def download(flag):
	# Local directory base
	lDirBase = 'E:/3G_KPI/'
	# Connect to correct FTP server depending on flag
	if flag == 'Huawei':
		# Huawei FTP credentials
		ftpHost = '172.16.102.95'
		ftpUserName = 'admBAN'
		ftpPassword = 'ADMbanglalink'
		rDir = '/3G-PRS/'
		customDate = (date.today()-timedelta(1)).strftime('%Y%m%d')
		ftp = ftpConnect(ftpHost,ftpUserName,ftpPassword)
		dlStatus = downloadFiles(flag, ftp, rDir, lDirBase, customDate)
	elif flag == 'Nokia':
		# Netact FTP credentials
		ftpHost = '10.10.26.8'
		ftpUserName = 'rnp01'
		ftpPassword = 'Blrnp123'
		rDir = '/var/opt/nokia/oss/global/shared/content3/scheduler/export/'
		customDate = (date.today()-timedelta(0)).strftime('%Y%m%d')
		ftp = ftpConnect(ftpHost,ftpUserName,ftpPassword)
		dlStatus = downloadFiles(flag, ftp, rDir, lDirBase, customDate)
# ---------------------------------------------------------------------------------------------------
# This is THE standard boilerplate that calls THE main() function
if __name__ == '__main__':
	main()		