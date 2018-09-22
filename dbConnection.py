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
# Import addin Libraries
import pymysql
# ---------------------------------------------------------------------------------------------------
# Define a connect() function
def connect():
	# Database Login Credentials
	host = 'localhost' # Change (localhost to <ip address> if necessary)
	port = '3306'	# Please don't change port value unless your server dictates
	userName = 'root' # Use database user name here
	password = 'skywalker' # use  database password here
	databaseName = '3g_kpi_db' # use database name here

	# try to connect to database
	try:
		connection = pymysql.connect(host, userName, password, databaseName)
	except:
		connection = False

	# Connection message
	if connection:
		print("\nUser [ {} ] is connected to [ {} ] mySQL database.".format(userName,databaseName), end='\n')
	else:
		print("\nUnable to connect to [ {} ] database. Exiting program.".format(databaseName), end='\n')

	return connection
# ---------------------------------------------------------------------------------------------------
# This is the standard boilerplate that calls the main() function
if __name__ == '__main__':
	main()