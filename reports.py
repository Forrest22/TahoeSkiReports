import json
from flask import Flask, render_template, url_for, request
app = Flask(__name__)

resorts = {}

with open("reports.json", "r") as jsonfile:
	resorts = json.load(jsonfile)
# print(json.dumps(resorts, sort_keys=True, indent=4))
# resorts = [
# 	{
# 		'name': 'Kirkwood',
# 		'snow_depth': 15.5,
# 		'lifts_open': 10,
# 		'total_lifts': 50,
# 		'last_updated': '2019-11-28'
# 	},
# 	{
# 		'name': 'Heavenly',
# 		'snow_depth': 35.5,
# 		'lifts_open': 18,
# 		'total_lifts': 65,
# 		'last_updated': '2019-11-28'
# 	},
# 	{
# 		'name': 'Northstar',
# 		'latest_report': {
# 			'snow_depth': 66.6,
# 			'lifts_open': 12,
# 			'total_lifts': 24,
# 			'last_updated': '2019-11-28'
# 		},
# 		'reports': [
# 			{
# 				'snow_depth': 56.6,
# 				'lifts_open': 2,
# 				'total_lifts': 24,
# 				'last_updated': '2019-11-20'
# 			},{
# 				'snow_depth': 56.6,
# 				'lifts_open': 2,
# 				'total_lifts': 24,
# 				'last_updated': '2019-11-20'
# 			},
# 		]
# 	},
# ]

# get the report each day, store it
# then get the latest report and send it in home

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',resorts=resorts)

@app.route('/compare')
def compare():
	return render_template('compare.html',resorts=resorts)

@app.route('/kirkwood')
@app.route('/heavenly')
@app.route('/northstar')
def viewResort():
	print(request.path)
	return render_template('viewResort.html')

@app.route('/about')
def about():
	return render_template('about.html',title="About Tahoe Ski Reports")

if __name__ == '__main__':
	app.run(debug=True)