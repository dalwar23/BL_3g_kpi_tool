import os
from datetime import datetime, date, time, timedelta
import time
# Import pymysql add-in
import pymysql
import dbConnection
import notificationEmailSender
def main():
	# Connect to Database
	connectionString = dbConnection.connect()
	# Get custom date for processing files and data
	dateSuffix = (date.today()-timedelta(1)).strftime('%Y%m%d')
	# Select a vendor
	vendorNames = [
					['Huawei', 'huawei_daily_3g_data_update'],
					['Nokia', 'nokia_daily_3g_data_update']
				  ]
	for vendor in vendorNames:
		# Send the mail
		notificationEmailSender.sendMail(connectionString,vendor[1],dateSuffix,vendor[0])
# ---------------------------------------------------------------------------------------------------
# This is THE standard boilerplate that calls THE main() function
if __name__ == '__main__':
	main()	