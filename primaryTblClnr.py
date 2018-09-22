#!/usr/bin/python -tt

# Author: Md Dalwar Hossain Arif
# Copy Right: Md Dalwar Hossain Arif
# License: Under GPU License
# Restriction: Proprietary information can't be removed
# For more information: www.arif23.com/python/privacy/
# ---------------------------------------------------------------------------------------------------
# Python Interpreter: 3.4.1
# mySQL Database Version: 5.6.11
# pymysql Version: 0.4
# ---------------------------------------------------------------------------------------------------
# Define a function that cleans all the primary tables
def tblClnr(connection,tableName):
	# Create a cursor to execute the DB query
	cursor = connection.cursor()

	# Create MYSQL database query string according to file name
	dbQuery = createQuery(tableName)

	# Execute SQL query using execute() method
	truncateTable = cursor.execute(dbQuery)

	# Commit data to DATABASE
	connection.commit()

	# Print message
	if truncateTable == 0:
		print('[ {} ] table truncated successfully.'.format(tableName), end='\n')
	else:
		print('[ {} ] table truncate ERROR!'.format(tableName),end='\n')
		pass
	# Close Cursor
	cursor.close();
# ---------------------------------------------------------------------------------------------------
# Define a function create Query to truncate tables
def createQuery(tableName):
	querySegment_1 = "TRUNCATE TABLE "
	querySegment_2 = tableName
	completeQuery = querySegment_1 + querySegment_2
	return completeQuery
# ---------------------------------------------------------------------------------------------------
# Define a function to trigger truncate
def truncate(connection,flag):
	if flag == 1:
		# Specify the list of tables to be truncated
		tableList = [
					# Primary tables
					'prs_primary',
					'prs_secondary',
					'netact_primary',
					'netact_secondary',
					'netact_ce_primary',
					'netact_ce_secondary'
					]
	elif flag == 2:
		# Specify the list of tables to be truncated
		tableList = [
					# Primary tables
					'prs_primary',
					'netact_primary',
					'netact_ce_primary'
					]		

	print("\n****** Truncating Table(s) ******\n", end='\n')
	currentQuery = 1
	totalQuery = len(tableList)
	
	# Now loop through the names and truncate the tables
	for tableName in tableList:
		# Print executing query message
		print("[ {} of {} ] -> ".format(currentQuery,totalQuery),end='')
		# Call a function that will clean all selected tables
		tblClnr(connection,tableName)
		currentQuery += 1
	
	print ("\n****** All listed table(s) truncated ******", end='\n')
# ---------------------------------------------------------------------------------------------------
# This is the standard boilerplate that calls the main() function
if __name__ == '__main__':
	main()