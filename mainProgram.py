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
from datetime import datetime, date, time, timedelta
import time
import shutil
# Import pymysql add-in
import pymysql
# Import custom library functions [these were supposed to be classes but i wrote them in functions]
import fileChecker
import dbConnection
import primaryTblClnr
import importCSV2DB
import tblOptimizer
import export2CSV
# ---------------------------------------------------------------------------------------------------
# Define a executeThreads() function to execute all threads
def executeThreads(connectionString,inputFileLocation):
	# Clear all primary tables
	flag = 1
	primaryTblClnr.truncate(connectionString,flag)

	# Import CSV files to DB tables
	importCSV2DB.csvimport(connectionString,inputFileLocation)

	# Optimize selected tables
	tblOptimizer.optimize(connectionString)
# ---------------------------------------------------------------------------------------------------
# Define a main() function
def main():
	# Start the program execution clock
	program_start_time = time.time()
	human_readable_time = time.strftime("%H:%M:%S", time.localtime(program_start_time))
	print("\nProgram clock started at -> [ {} ]".format(str(human_readable_time)),end='\n')
	
	# Print an initialization message
	print("\nInitializing program..........\n",end='\n')

	# Introduce input file locations
	inputFileLocation = 'D:/3G_KPI/INPUT/' 	# Change this string according to input files' location
	rawFileLocation = 'E:/3G_KPI/'
	outputDirectory = 'D:/3G_KPI/OUTPUT'	# No forward slash needed

	# Get custom date for processing files and data
	dateSuffix = (date.today()-timedelta(1)).strftime('%Y%m%d')
	
	# Check whether files are present or not, if present then copy them to input directory
	fileCheckStatus = fileChecker.checkFiles(rawFileLocation,inputFileLocation,dateSuffix)
	if fileCheckStatus == 1:
		# Create a database connection
		print("\n****** Connecting to mySQL Database ******", end='\n')
		# Connect to Database
		connectionString = dbConnection.connect()
		# Connection complete message
		print("\n****** Connected to mySQL Database ******", end='\n\n')		
		# Call execute function to execute necessary threads
		executeThreads(connectionString,inputFileLocation)
		# Export results to csv files
		export2CSV.exportData(connectionString,outputDirectory,dateSuffix)
	else:
		print('Files doesn\'t exists! Please upload the required files and try again later.')
	# Close Database Connection
	connectionString.close()
	# Print program execution time message
	program_elapsed_sec = (time.time() - program_start_time)
	program_elapsed_min = round((program_elapsed_sec / 60),2)
	print('\nProgram executed in [ {} ] minutes.'.format(program_elapsed_min), end='\n')

	# Print exit message
	print('Exiting..........', end='\n')
# ---------------------------------------------------------------------------------------------------
# This is THE standard boilerplate that calls THE main() function
if __name__ == '__main__':
	main()