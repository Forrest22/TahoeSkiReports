from flask import Flask, render_template, url_for
app = Flask(__name__)

resorts = [
	{
		'resort': 'Kirkwood',
		'snow_depth': 15.5,
		'lifts_open': 10,
		'total_lifts': 50,
		'last_updated': '2019-11-28'
	},
	{
		'resort': 'Heavenly',
		'snow_depth': 35.5,
		'lifts_open': 18,
		'total_lifts': 65,
		'last_updated': '2019-11-28'
	},

]

@app.route('/')
@app.route('/home')
def hello_world():
    return render_template('home.html',resorts=resorts)

@app.route('/about')
def about():
	return render_template('about.html',title="About Tahoe Ski Reports")

if __name__ == '__main__':
	app.run(debug=True)