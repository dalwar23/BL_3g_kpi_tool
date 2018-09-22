#!/usr/bin/python -tt

# Author: Md Dalwar Hossain Arif
# Copy Right: Md Dalwar Hossain Arif
# License: Under GPU License
# Restriction: Proprietary information can't be removed
# For more information: www.pysource.org/privacy
# ---------------------------------------------------------------------------------------------------
# Python Interpreter: 3.4.1
# mySQL Database Version: 5.6.11
# pymysql Version: 0.4
# ---------------------------------------------------------------------------------------------------
# Import Built-In Libraries
import os
# Import custom libraries
import primaryTblClnr
# ---------------------------------------------------------------------------------------------------
# Define a function to execute import query
def executeQuery(connection,inputDirectory,inputFile,fileType):
	# Prepare a cursor object using cursor() method
	cursor = connection.cursor()
	# Create MYSQL database query string according to file name
	dbQuery = createQuery(inputDirectory,inputFile,fileType)
	# Execute SQL query using execute() method
	try:
		loadData = cursor.execute(dbQuery)
	except:
		print('CSV import Failed!! Please ')
	# Commit data to DATABASE
	connection.commit()
	# Close Cursor
	cursor.close();

	# Print message
	if loadData:
		print("[ {} ] file imported successfully.".format(inputFile), end='\n')
	else:
		print("Import Error! [ {} ]".format(inputFile), end='\n')
# ---------------------------------------------------------------------------------------------------
# Define a function to create query
def createQuery(inputDirectory,inputFile,fileType):
	if fileType == 'PRS':
		tableName = 'prs_primary'
		ignoredLines = 7
	elif fileType == 'NETACT':
		tableName = 'netact_primary'
		ignoredLines = 1
	elif fileType == 'NETACT_CE':
		tableName = 'netact_ce_primary'
		ignoredLines = 3		
	else:
		print('Unknown file type - PRS/NETACT',end='\n')
	# Create query to load data to right table
	querySegment_1 = "LOAD DATA INFILE   '"
	querySegment_2 = inputDirectory + inputFile + "'"
	querySegment_3 = " INTO TABLE " + tableName
	querySegment_4 = """ FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\\n' IGNORE """
	querySegment_5 = str(ignoredLines) # Change this value if needed to ignore more then 1 line
	querySegment_6 = " LINES"

	# Now complete query by joining all the segments togather
	completeQuery = querySegment_1 + querySegment_2 + querySegment_3 + querySegment_4 + querySegment_5 + querySegment_6
	# return complete query
	return completeQuery
# ---------------------------------------------------------------------------------------------------
# Define a function to delete unnecessary data in mySQL DB
def dataCleanup(connection,tableName):
	# Now delete corresponding lines from DB
	# Prepare a cursor object using cursor() method
	cursor = connection.cursor()
	# Create MYSQL database query string according to file name
	dbClenaupQuery = cleanupQuery(tableName)
	# Execute SQL query using execute() method
	try:
		cleanData = cursor.execute(dbClenaupQuery)
		if cleanData:
			print("\nCleaned up table -> [ {} ]".format(tableName), end='\n')
		else:
			print('Can\'t or no need to clean up table -> [ {} ]'.format(tableName))
	except:
		print('Can\'t or no need to clean up table -> [ {} ]'.format(tableName))
	# Commit data to DATABASE
	connection.commit()
	# Close Cursor
	cursor.close();
# ---------------------------------------------------------------------------------------------------
# Define a function to create cleanup query
def cleanupQuery(tableName):
	# Create query to load data to right table
	querySegment_1 = "DELETE "
	querySegment_2 = "FROM " + tableName
	querySegment_3 = " WHERE TIME_ LIKE "
	querySegment_4 = "'Total%'"
	# Now complete query by joining all the segments togather
	completeQuery = querySegment_1 + querySegment_2 + querySegment_3 + querySegment_4
	# return complete query
	return completeQuery
# --------------------------------------------------------------------------------------------------
# Define a function to execute transfer data from view to table
def trasferViewData2Table(connection,item):
	# Prepare a cursor object using cursor() method
	cursor = connection.cursor()
	# Create MYSQL database query string according to item
	dataTransferQuery = createTransferQuery(item)
	try:
		# Execute SQL query using execute() method
		transferData = cursor.execute(dataTransferQuery)
	except:
		# Print Error message
		print("ERROR!")
	# Commit data to DATABASE
	connection.commit()
	# Close Cursor
	cursor.close()
	# Print message
	if transferData:
		print("[ {} ] -> [ {} ] -> OK".format(item[0],item[1]), end='\n')
	else:
		print("Data transfer Error! on table -> [ {} ]".format(item[1]), end='\n')
# ---------------------------------------------------------------------------------------------------
# Define a function createTransferQuery(item)
def createTransferQuery(item):
	viewName = item[0]
	tableName = item[1]
	querySegment_1 = "INSERT IGNORE INTO "
	querySegment_2 = tableName
	querySegment_3 = " SELECT * FROM "
	querySegment_4 = viewName
	completeQuery = querySegment_1 + querySegment_2 + querySegment_3 + querySegment_4
	#print(completeQuery, end='\n')
	return completeQuery	
# ---------------------------------------------------------------------------------------------------
# Define a function to delete input files
def deleteInputFiles(inputDirectory,inputFile):
	# Now delete corresponding input file
	filePath = inputDirectory + inputFile
	try:
		os.remove(filePath)
		print('Inputfile [ {} ] deleted.'.format(inputFile),end='\n')
	except OSError:
		print('Error: {} - {}.'.format(filename,strerror),end='\n')
# ---------------------------------------------------------------------------------------------------
# Define import function
def csvimport(connection,inputDirectory):
	# Create an empty list that will store the file names from input directory
	inputFileList = []
	for file in os.listdir(inputDirectory):
		if file.endswith('.csv'):
			inputFileList.append(file)
	# Print csv import message
	currentQueryCount = 1
	totalQueryCount = len(inputFileList)
	print("\n****** Importing CSV files to DB ******\n", end='\n')
	# Call a function that will import CSV to database
	for fileName in inputFileList:
		inputFile = fileName.upper()
		# Determine input file type - daily/hourly ?
		if 'PRS' in inputFile:
			fileType = 'PRS'
		elif 'NETACT' in inputFile:
			if inputFile.startswith('NETACT') and 'CE' not in inputFile:
				fileType = 'NETACT'
			elif inputFile.startswith('NETACT') and 'CE' in inputFile:
				fileType = 'NETACT_CE'
		# Print executing query message
		print("[ {} of {} ] -> ".format(currentQueryCount,totalQueryCount), end='')
		executeQuery(connection,inputDirectory,inputFile,fileType)
		# Increase query count value
		currentQueryCount += 1
	# Delete unnecessary lines - (last line of every PRS file to be exact)
	print('\n****** Trying to delete unnecessary data from DB ******', end='\n')
	tableNameList = ['prs_primary','netact_primary']
	for tableName in tableNameList:
		dataCleanup(connection,tableName)
	# Once data transfer is done - truncate the primary tables
	flag = 2
	#primaryTblClnr.truncate(connection,flag)		
	print("\n****** All unnecessary data cleaned from DB ******", end='\n')
	# Now load refined data from view to secondary table
	print("\nTransfering data......\n",end='\n')
	srcNDstList = [
		['prs_view_primary','prs_secondary'],
		['netact_view_primary','netact_secondary'],
		['netact_ce_view_primary','netact_ce_secondary'],
		['prs_3g_pre_data_update','huawei_daily_3g_pre_data_update'],
		['prs_3g_data_update','huawei_daily_3g_data_update'],
		['netact_3g_pre_data_update','nokia_daily_3g_pre_data_update'],
		['netact_3g_data_update','nokia_daily_3g_data_update'],
		['prs_3g_data_update','huawei_nokia_daily_report'],
		['netact_3g_data_update','huawei_nokia_daily_report'],
		['netact_3g_data_update_rnc_wise','huawei_nokia_rnc_data'],
		['prs_3g_data_update_rnc_wise','huawei_nokia_rnc_data'],
		['vimp_dashboard_report','vimpelcom_report'],
		['bh_by_date','busy_hours_by_date'],
		['prs_3g_common_data','3g_common_kpi'],
		['netact_3g_common_data','3g_common_kpi']
	]
	# loop through list and transfer data from view to table
	for item in srcNDstList:
		trasferViewData2Table(connection,item)
	print("\n****** All CSV files imported to DB ******", end='\n')
	# Delete input files
	print("\n****** Deleting input files ******\n", end='\n')
	for fileName in inputFileList:
		inputFile = fileName
		deleteInputFiles(inputDirectory,inputFile)
	print("\n****** All input files deleted ******")
# ---------------------------------------------------------------------------------------------------
# This is the standard boilerplate that calls the main() function
if __name__ == '__main__':
	main()