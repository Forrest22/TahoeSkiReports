from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from datetime import date


heavenly = "https://www.skiheavenly.com/"
kirkwood = "https://www.kirkwood.com/"
northstar = "https://www.northstarcalifornia.com/"

snowandweatherreports = "the-mountain/mountain-conditions/snow-and-weather-report.aspx"
terrainandliftstatus = "the-mountain/mountain-conditions/terrain-and-lift-status.aspx"

driver = webdriver.Firefox(executable_path="./geckodriver")

resorts = {
	'heavenly': heavenly,
	# 'kirkwood': kirkwood,
	# 'northstar': northstar
}

# def initiateDriver():
	# Makes headless firefox using geckodriver
	# options = Options()
	# options.headless = True
	# driver = webdriver.Firefox(options=options, executable_path="geckodriver-v0.26.0-linux64/geckodriver")
	# return driver

def getMostRecentReports():
	reports = []

	for resort in resorts:
		# Sets the driver to the relevant page
		getPage(resorts[resort]+snowandweatherreports)
		# Appends report info to reports
		reports.append(parseSnowPage(resort))

	print(reports)

	return reports

def getPage(site):
	driver.get(site)
	return driver.page_source

def parseSnowPage(resort):
	report = {
		"resort": resort,
		"overnight": None,
		"24_hr": None,
		"48_hr": None,
		"base_depth": None,
		"season_total": None,
		"last_updated": date.today(),
		"units": "in."
	}

	# Parse page with bs4
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	snowMeasurements = soup.findAll("h5", {"class": "snow_report__metrics__measurement c78__total1--v1"})

	# Get info from each section	
	report["overnight"] = int((snowMeasurements[0].get_text().split("in")[0]))
	report["24_hr"] = int((snowMeasurements[1].get_text().split("in")[0]))
	report["48_hr"] = int((snowMeasurements[2].get_text().split("in")[0]))
	report["base_depth"] = int((snowMeasurements[3].get_text().split("in")[0]))
	report["season_total"] = int((snowMeasurements[4].get_text().split("in")[0]))
	return

def parseLiftPage(page):
	return

def test():
	driver.get('https://www.snow.com/moun Nonetainconditions/snowandweatherreports.aspx')

	# Parses with bs4
	soup = BeautifulSoup(driver.page_source, 'html.parser')

	# soup.find('table')
	# soup = BeautifulSoup(url_get.content, 'html.parser')
	# The following is dependant on the "lmxl" library
	# soup = BeautifulSoup(url_get.content, 'lmxl')

	# print(soup.prettify())
	# print(soup.findAll("h1", {"class": "hero__content__title reverse"}))
	# print(soup.findAll("ul", {"class": "snow_report__metrics col-xs-12"}))

	for section in soup.findAll("h5", {"class": "snow_report__metrics__measurement c78__total1--v1"}):
		# for section in measurements:
		# print(section)
		print((section.get_text().split("in")[0]))
	# Get info from each section
	# EX)
			# "latest_report": {
			# "snow_depth": 15.5,
			# "lifts_open": 10,
			# "total_lifts": 50,
			# "last_updated": "2019-11-28",
			# "units": "in."
	# driver.quit()
	return

if __name__ == '__main__':
	getMostRecentReports()
	# test()
	
	driver.quit()