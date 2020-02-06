import json
import sys
import os
from datetime import date, datetime
from flask import Flask, render_template, url_for, request

sys.path.insert(0, os.getcwd()+'/src/')
import reportscanner

app = Flask(__name__)
# app.config["SERVER_NAME"] = 'tahoeskireports.forrestthe.dev:5000'

global notTheDB 
notTheDB = {
	"resorts": [],
	"last_updated_time": "10:00"
}

# with open("reports.json", "r") as jsonfile:
# 	notTheDB = json.load(jsonfile)

def lastUpdatedHoursAgo():
	global notTheDB
	try:
		t1 = datetime.strptime(notTheDB["last_updated_time"], "%H:%M")
		t2 = datetime.strptime(datetime.now().strftime("%H:%M"), "%H:%M")
		tdelta =  t2 - t1
		print(tdelta.seconds//3600)
		return tdelta.seconds//3600
	except Exception as e:
		print("Error checking time")
		return  0

# get the report each day, store it
# then get the latest report and send it in home
# updates reports of resorts if old, async
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
			try:
				latestReports = reportscanner.getMostRecentReports()
				notTheDB["last_updated_time"] = datetime.now().strftime("%H:%M")
				# In notTheDB, copies old report, replaces with new report
				# For each resort take the latest report and insert it into reports
				# Then find the latest report that matches resort["name"]
				# And copy latestReports[resort["name"]] into notTheDB["resorts"]
				tempReports = {}
				for resort in notTheDB["resorts"]:
					i = None
					thisResort = resort["name"]
					print("Getting report for " + thisResort)
					tempReports[thisResort] = resort["latest_report"]

					for x in range(0,len(notTheDB["resorts"])):
						if notTheDB["resorts"][x]["name"] == thisResort:
							i = x
							break

					# Gets matching resort and inserts the old report
					# Inserts old report into reports
					notTheDB["resorts"][i]["reports"].insert(0,tempReports[thisResort])

					# Finds the corresponding latestReport and replaces latest_report
					notTheDB["resorts"][i]["latest_report"] = latestReports[thisResort]

				with open("reports.json", "w") as jsonFile:
					notTheDB = json.dump(notTheDB, jsonFile)

				print("Background update complete.")
				os._exit(0)
			except Exception as e:
				print("Error occurred updating")
				os._exit(0)
				raise e

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
	# print(notTheDB)
	return render_template('home.html', resorts=notTheDB, title="Home")

@app.route('/compare')
def compare():
	global notTheDB
	return render_template('compare.html', resorts=notTheDB, title="Compare")

@app.route('/kirkwood')
@app.route('/heavenly')
@app.route('/northstar')
def viewResort():
	resortName = request.path[1:].capitalize()
	for x in range(0,len(notTheDB["resorts"])):
		if notTheDB["resorts"][x]["name"] == resortName:
			i = x
			break

	return render_template('viewResort.html', resort=notTheDB["resorts"][x])

@app.route('/about')
def about():
	return render_template('about.html',title="About")

if __name__ == '__main__':	
	# Loads initial data
	with open("reports.json", "r") as jsonFile:
		notTheDB = json.load(jsonFile)
	
	# Updates the reports
	notTheDB = updateReports()

	app.run(debug=True)