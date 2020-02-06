import json
import sys
import os
from datetime import date, datetime
from flask import Flask, render_template, url_for, request

sys.path.insert(0, os.getcwd()+'/src/')
import reportscanner

app = Flask(__name__)
global notTheDB 
notTheDB = {
	"resorts": [],
	"last_updated_time": "00:00"
}

# with open("reports.json", "r") as jsonfile:
# 	notTheDB = json.load(jsonfile)

def lastUpdatedHoursAgo():
	global notTheDB
	try:
		t1 = datetime.strptime(notTheDB["last_updated_time"], "%H:%M")
		t2 = datetime.strptime(datetime.now().strftime("%H:%M"), "%H:%M")
		tdelta =  t2 - t1
		# print(tdelta.seconds//3600)
		return tdelta.seconds//3600
	except Exception as e:
		print("Error checking time")
		return  0

# get the report each day, store it
# then get the latest report and send it in home
# updates reports of resorts if old
# Note to self: make this async with os.fork()
def updateReports():
	global notTheDB
	if lastUpdatedHoursAgo() > 4:
		# Gets current nodb values
		with open("reports.json", "r") as jsonFile:
			notTheDB = json.load(jsonFile)

		# Forks updating db to not hold up request
		pid = os.fork()
		
		if pid == 0:
			print("Starting background update.")

			# Get the most recent report, update last_updated_time
			# try:
			latestReports = reportscanner.getMostRecentReports()
			notTheDB["last_updated_time"] = datetime.now().strftime("%H:%M")
			print(latestReports)
			# In notTheDB, copies old report, replaces with new report
			# For each resort take the latest report and insert it into reports
			# Then find the latest report that matches resort["name"]
			# And copy latestReports[resort["name"]] into notTheDB["resorts"]
			tempReports = {}
			for i, resort in enumerate(notTheDB["resorts"]):
				thisResort = resort["name"]
				print("thisResort: " + thisResort)
				tempReports[thisResort] = resort["latest_report"]
				# Gets matching resort and inserts the old report
				# Inserts old report into reports
				# print("Inserting old " + str(tempReports[thisResort]) + " report into ['reports']")
				notTheDB["resorts"][i]["reports"].insert(0,tempReports[thisResort])
				# Finds the corresponding latestReport and replaces latest_report
				# print(len(latestReports))
				notTheDB["resorts"][i]["latest_report"] = latestReports[thisResort]
				print(notTheDB["resorts"][i]["latest_report"])


			# print(tempReports)
			for resort in notTheDB["resorts"]:
				print(resort["latest_report"])

			# notTheDBs

			with open("reports.json", "w") as jsonFile:
				notTheDB = json.dump(notTheDB, jsonFile)

			print("Background update complete.")
			os._exit(0)
			# except Exception as e:
			# 	print("Error occurred updating")
			# 	os._exit(0)
			# 	raise e

	else:
		with open("reports.json", "r") as jsonFile:
			notTheDB = json.load(jsonFile)
			
	return notTheDB

@app.route('/')
@app.route('/home')
def home():
	global notTheDB
	# if(lastUpdatedHoursAgo() > 6):
	# 	print("Update")

	notTheDB = updateReports()
	print(notTheDB)
	return render_template('home.html', resorts=notTheDB, title="Home")

@app.route('/compare')
def compare():
	global notTheDB
	return render_template('compare.html', resorts=notTheDB, title="Compare")

@app.route('/kirkwood')
@app.route('/heavenly')
@app.route('/northstar')
def viewResort():
	pageName = request.path[1:].capitalize()
	return render_template('viewResort.html', resort=pageName)

@app.route('/about')
def about():
	return render_template('about.html',title="About")

if __name__ == '__main__':
	# website_url = 'reports.forrestthe.dev:5000'
	# app.config['SERVER_NAME'] = website_url
	notTheDB = updateReports()
	app.run(debug=True)