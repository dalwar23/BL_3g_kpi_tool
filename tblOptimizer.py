#!/usr/bin/python -tt

# Author: Md Dalwar Hossain Arif
# Copy Right: Md Dalwar Hossain Arif
# License: Under GPU License
# Restriction: Proprietary information can't be removed
# For more information: www.pysource.com/privacy/
# ---------------------------------------------------------------------------------------------------
# Python Interpreter: 3.4.1
# mySQL Database Version: 5.6.11
# pymysql Version: 0.4
# ---------------------------------------------------------------------------------------------------
# Define a function executeQuery(connection,tableName)
def executeQuery(connection,tableName):
	# Prepare a cursor object using cursor() method
	cursor = connection.cursor()
	# Create MYSQL database query string according to file name
	dbQuery = createQuery(tableName)
	# Execute SQL query using execute() method
	optimizeTable = cursor.execute(dbQuery)
	# Commit data to DATABASE
	connection.commit()
	# Print message
	if optimizeTable:
		print('[ {} ] - table optimized.'.format(tableName), end='\n')
	else:
		print('[ {} ] - table optimization ERROR!'.format(tableName), end='\n')
		pass
	# Close Cursor
	cursor.close();
# Define a function createQuery(item)
def createQuery(tableName):
	querySegment_1 = "OPTIMIZE TABLE "
	querySegment_2 = tableName
	completeQuery = querySegment_1 + querySegment_2
	return completeQuery
# --------------------------------------------------------------------------------------------------
# Define optimize function
def optimize(connection):
	# Create table list to truncate
	tableList = ['prs_primary', 'prs_secondary', 
				'netact_primary','netact_secondary',
				'netact_ce_primary','netact_ce_secondary',
				'huawei_daily_3g_data_update','nokia_daily_3g_data_update',
				'huawei_nokia_daily_report'
				]
	print("\n****** Optimizing database tables ******\n", end='\n')
	# Count total query
	totalQuery = len(tableList)
	# Set current query
	currentQuery = 1
	# Extract data form view and store into tables
	for tableName in tableList:
		# Print executing query message
		print("[ {} of {} ] -> ".format(currentQuery,totalQuery), end='')
		# Call a function that will optimize all tables
		executeQuery(connection,tableName)
		currentQuery += 1
	print("\n****** Database table optimization completed ******", end='\n')
# ---------------------------------------------------------------------------------------------------
# This is THE standard boilerplate that calls THE main() function
if __name__ == '__main__':
	main()