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

# Import Libraries
import os
import sys
import pymysql
import csv
# -------------------------------------------------------------------------------------------------------
# Define a function executeExportQuery()
def executeExportQuery(connectionString, outputDirectory, item, customDate):
	# Prepare a cursor object using cursor() method
	cursor = connectionString.cursor()
	# Create mySQL database query
	dbQuery = createQuery(item[0])
	# Print executing query message
	print("Executing query -> ",end='')
	# Execute SQL query using execute() method
	result = cursor.execute(dbQuery)
	# Get the total number of rows
	totalRows = result
	# using fetchone()/fetchmany()/fetchall() methods
	# [below line is not necessary if CURSOR method used to view data]**
	#data = cursor.fetchmany(size=5)
	# Create a csv file name
	outPutFileName = outputDirectory + item[1] + customDate + '.csv'
	# Open CSV file and write the result
	FILE = open(outPutFileName,'w', newline='')
	output = csv.writer(FILE, dialect='excel')
	if FILE:
		print("Creating -> [ {} ] file...".format(item[1]+customDate))
	else:
		print("Unable to create CSV file.","Exiting...", sep='\n')
	# Get headers from the table to a list
	headers = []
	for col in cursor.description:
		headers.append(col[0])
	output.writerow(headers)
	# Create a counter
	counter = 1
	# Now write rest of the rows [CURSOR method used]**
	for row in cursor:
		percentage = round((counter/totalRows)*100,2)
		# Length of characters in percentage
		noOfchars = len(str(percentage))
		# Below line outputs to file
		output.writerow(row)
		# Show percentage message on screen
		infoMessage = '% completed'
		# Total character to delete (backspace)
		totalChars = noOfchars + len(infoMessage)
		# Print out the percentage of work done on screen
		sys.stdout.write('{}{}'.format(str(percentage),infoMessage))
		sys.stdout.flush()
		sys.stdout.write('\b'*totalChars)
		counter +=1		
	print("\n[ {} ] file created.\n".format(item[1]+customDate), end='\n')
	# Close Cursor
	cursor.close();
	# Close writing to file
	FILE.close()
# End of function executeQuery(c=connection, t=tableName)
# -----------------------------------------------------------------------------------------------------
# Define a createQuery(tableName) function
def createQuery(tableName):
	querySegment_1 = """SELECT * FROM """
	querySegment_2 = tableName
	completeQuery = querySegment_1 + querySegment_2
	return completeQuery
# --------------------------------------------------------------------------------------------------
# Define a main() function
def exportData(connectionString,outputDirectoryBase,dateSuffix):
	# Print welcome message
	print("\nInitializing data export to CSV files...\n",end='\n')
	
	# Create a list of table that you want to export
	tableNameList = [ # Huawei files 
					 ['prs_secondary','3G_Raw_','Huawei'],
					 ['prs_3g_cell_hourly','3G_Cell_Hourly_','Huawei'],
					 ['prs_3g_cell_daily','3G_Cell_Daily_','Huawei'],
					 ['prs_3g_node_b_hourly','3G_NodeB_Hourly_','Huawei'],
					 ['prs_3g_node_b_daily','3G_NodeB_Daily_','Huawei'],
					 ['prs_3g_rnc_hourly','3G_RNC_Hourly_','Huawei'],
					 ['prs_3g_rnc_daily','3G_RNC_Daily_','Huawei'],
					 ['prs_3g_network_hourly','3G_Network_Hourly_','Huawei'],
					 ['prs_3g_network_daily','3G_Network_Daily_','Huawei'],
					 ['prs_3g_data_update','3G_Data_Update_','Huawei'],
					 ['prs_3g_data_update_rnc_wise','3G_Data_Update_RNC_Wise_','Huawei'],
					 ['prs_3g_cell_daily_tracing','3G_Cell_Daily_Tracing_','Huawei'],
					 # Netact file
					 ['netact_secondary','3G_Raw_','Netact'],
					 ['netact_3g_cell_hourly','3G_Cell_Hourly_','Netact'],
					 ['netact_3g_cell_daily','3G_Cell_Daily_','Netact'],
					 ['netact_3g_node_b_hourly','3G_NodeB_Hourly_','Netact'],
					 ['netact_3g_node_b_daily','3G_NodeB_Daily_','Netact'],
					 ['netact_3g_rnc_hourly','3G_RNC_Hourly_','Netact'],
					 ['netact_3g_rnc_daily','3G_RNC_Daily_','Netact'],
					 ['netact_3g_network_hourly','3G_Network_Hourly_','Netact'],
					 ['netact_3g_network_daily','3G_Network_Daily_','Netact'],
					 ['netact_3g_data_update','3G_Data_Update_','Netact'],
					 ['netact_3g_data_update_rnc_wise','3G_Data_Update_RNC_Wise_','Netact'],
					 ['netact_3g_cell_daily_tracing','3G_Cell_Daily_Tracing_','Netact'],
					 # Vimpelcom Report
					 ['vimp_dashboard_report','vimpelcom_report','Vimpelcom']
					]
	# Count total query
	totalQuery = len(tableNameList)

	# Set current query
	currentQuery = 1
	for item in tableNameList:
		# Create exact path
		pathSep = '/'
		outputDirectory = outputDirectoryBase + pathSep + item[2] + pathSep + dateSuffix + pathSep
		# Create folder if it doesn't exist
		try:
			if not os.path.exists(outputDirectory): os.makedirs(outputDirectory)
		except:
			print('Folder creation Error!', end='\n')
		# Print executing query message
		print("[ {} ] -> [ {} of {} ] -> ".format(item[2], currentQuery, totalQuery), end='')
		executeExportQuery(connectionString,outputDirectory,item, dateSuffix)
		currentQuery += 1
# End of main() function
# ---------------------------------------------------------------------------------------------------
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main()
# ---------------------------------------------------------------------------------------------------