#!/usr/bin/python -tt

# Author: Md Dalwar Hossain Arif
# Copy Right: Md Dalwar Hossain Arif
# Lisence: GPU License
# More Information: www.pySource.org/privacy/
# ---------------------------------------------------------------------------------------
# Python Interpreter: 3.4.1
# ---------------------------------------------------------------------------------------
# Import built-in library
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Define main() function
def sendMail(connectionString,tableName,dateSuffix,vendorName):
	# Prepare a cursor object using cursor() method
	cursor = connectionString.cursor()
	# Create mySQL database query
	dbQuery = createQuery(tableName,dateSuffix)
	# Print executing query message
	print("Executing query -> ",end='')
	# Execute SQL query using execute() method
	result = cursor.execute(dbQuery)
	# ------------------------------------------------------------------------------------
	# Introduce SMTP server and login credentials
	smtpHost = '172.16.10.174' # 587 -> Non-Secure port , 465 -> Secure Port
	username = ''
	password = ''
	# Introduce sender and recipient of the e-mail
	sender = 'noreply-qosdatabank@banglalinkgsm.com'
	emailTo = 'mdrhasan@banglalinkgsm.com'
	emailCc = ['kalam@banglalinkgsm.com','marif@banglalinkgsm.com','mmansur@banglalinkgsm.com','aaharar@banglalinkgsm.com','ekkabir@banglalinkgsm.com']
	#emailTo = 'marif@banglalinkgsm.com'
	#emailCc = ['mmansur@banglalinkgsm.com']
	subject = vendorName + ' 3G KPI Data Update [Computer generated e-mail]'
	# Create Message container - Correct MIME type is multipart/alternative
	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = emailTo
	msg['Cc'] = ','.join(emailCc)
	recipients = [emailTo] + emailCc
	# Create the body of the message (a plain-text and an HTML version)
	#palinText = '''\
	#Dear Concern,\nPlease be informed that, IT data has been uploaded successfully.\nPlease do not reply, 
	#This is a computer generated notification email.\n\n---\n\nQOSAPPSRVR
	#'''
	html = """\
	<html>
		<head>
			<title>E-mail Message</title>
			<style>
				body{
					font-family: 'Segoe UI',Tahoma, Verdana;
					font-weight: Normal;
					font-size: 85%;
				}
				td{
					border: 1px solid black;
					text-align: right;
					border-collapse: collapse;
					padding:5px;
				}
			</style>
		</head>
		<body>
			<p>
				Dear Concern,
			</p>
			<p>
				Please be informed that, """ + vendorName +  """ 3G data has been updated successfully.<br/>
				<br/>
				<strong>3G KPI Data</strong>
				<br/><br/>
				<table border='1px solid black' cellspacing='1' cellpadding='1'>
	"""
	for row in cursor:
		tableData ="""
		<tr>
			<td>Date</td>
				<td colspan='2'>"""+str(row[0])+"""</td>
			</tr>
			<tr>
				<td>CS_NBH</td>
				<td colspan='2' >"""+str(row[2])+"""</td>
			</tr>
			<tr>
				<td>PS_NBH</td>
				<td colspan='2'>"""+str(row[3])+"""</td>
			</tr>
			<tr>
				<td>CS_AMR_TRAFFIC_ERL</td>
				<td>"""+str(row[4])+"""</td>
				<td>"""+str(row[20])+"""</td>
			</tr>
			<tr>
				<td>CS_VP_TRAFFIC_ERL</td>
				<td>"""+str(row[5])+"""</td>
				<td>"""+str(row[21])+"""</td>
			</tr>
			<tr>
				<td>R99_PS_TRAFFIC_MB</td>
				<td>"""+str(row[6])+"""</td>
				<td>"""+str(row[22])+"""</td>
			</tr>
			<tr>
				<td>HSDPA_TRAFFIC_MB</td>
				<td>"""+str(row[7])+"""</td>
				<td>"""+str(row[23])+"""</td>
			</tr>
			<tr>
				<td>HSUPA_TRAFFIC_MB</td>
				<td>"""+str(row[8])+"""</td>
				<td>"""+str(row[24])+"""</td>
			</tr>
			<tr>
				<td>HSPA_TRAFFIC_MB</td>
				<td>"""+str(row[9])+"""</td>
				<td>"""+str(row[25])+"""</td>
			</tr>
			<tr>
				<td>CE_CONG_RATE</td>
				<td>"""+str(row[10])+"""</td>
				<td>"""+str(row[26])+"""</td>
			</tr>
			<tr>
				<td>CS_AMR_DROP_RATE</td>
				<td>"""+str(row[11])+"""</td>
				<td>"""+str(row[27])+"""</td>
			</tr>
			<tr>
				<td>CS_VP_DROP_RATE</td>
				<td>"""+str(row[12])+"""</td>
				<td>"""+str(row[28])+"""</td>
			</tr>
			<tr>
				<td>PS_R99_DROP_RATE</td>
				<td>"""+str(row[13])+"""</td>
				<td>"""+str(row[29])+"""</td>
			</tr>
			<tr>
				<td>HSDPA_DROP_RATE</td>
				<td>"""+str(row[14])+"""</td>
				<td>"""+str(row[30])+"""</td>
			</tr>
			<tr>
				<td>HSUPA_DROP_RATE</td>
				<td>"""+str(row[15])+"""</td>
				<td>"""+str(row[31])+"""</td>
			</tr>
			<tr>
				<td>CS_CSSR</td>
				<td>"""+str(row[16])+"""</td>
				<td>"""+str(row[32])+"""</td>
			</tr>
			<tr>
				<td>PS_CSSR</td>
				<td>"""+str(row[17])+"""</td>
				<td>"""+str(row[33])+"""</td>
			</tr>
			<tr>
				<td>CS_IRAT_HOSR</td>
				<td>"""+str(row[18])+"""</td>
				<td>"""+str(row[34])+"""</td>
			</tr>
			<tr>
				<td>PS_IRAT_HOSR</td>
				<td>"""+str(row[19])+"""</td>
				<td>"""+str(row[35])+"""</td>
			</tr>
			<tr>
				<td>HSDPA_THPT_PERCELL</td>
				<td colspan='2'>"""+str(row[36])+"""</td>
			</tr>
			<tr>
				<td>HSDPA_THPT_PERUSER</td>
				<td colspan='2'>"""+str(row[37])+"""</td>
			</tr>
			<tr>
				<td>HSUPA_THPT_PERCELL</td>
				<td colspan='2'>"""+str(row[38])+"""</td>
			</tr>
			<tr>
				<td>HSUPA_THPT_PERUSER</td>
				<td colspan='2'>"""+str(row[39])+"""</td>
			</tr>
		"""
	html += tableData
	html +="""
				</table>
				>> Please do not reply, This is a computer generated notification email.<br/>
			</p>
			<p class='sign'>
				---<br/>
				QOS-DATABANK
			</p>
		</body>
	</html>
	"""
	# Record the MIME types of both parts - text/plain and text/html
	#partOne = MIMEText(palinText,'plain')
	partTwo = MIMEText(html,'html')
	# Attach parts into message container
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is the best and preffered
	#msg.attach(partOne)
	msg.attach(partTwo)
	# Send e-mail via SMTP host and credentials
	server = smtplib.SMTP(smtpHost,25)
	server.ehlo()
	#server.starttls() # use this line for tls - if the port is set to non-secure and smtplib.SMTP is on
	#server.ehlo()
	#try:
	#	server.login(username,password)
	#except:
	#	print('Username, Password combination invalid', end='\n')
	try:
		server.sendmail(sender,recipients,msg.as_string())
	except:
		print('An Error! occured while sending e-mail')
	else:
		print('Email sent to {} recipients'.format(len(recipients)),end ='\n')
	server.quit()
# -----------------------------------------------------------------------------------------------------
# Define a createQuery(tableName) function
def createQuery(tableName, dateSuffix):
	querySegment_1 = """SELECT * FROM """
	querySegment_2 = tableName
	querySegment_3 = """ WHERE DATES = '"""
	querySegment_4 = dateSuffix + "'"
	completeQuery = querySegment_1 + querySegment_2 + querySegment_3 + querySegment_4
	return completeQuery