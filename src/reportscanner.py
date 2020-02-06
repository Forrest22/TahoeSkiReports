from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from datetime import date, datetime
import sys
import os

heavenly = "https://www.skiheavenly.com/"
kirkwood = "https://www.kirkwood.com/"
northstar = "https://www.northstarcalifornia.com/"

snowAndWeatherReports = "the-mountain/mountain-conditions/snow-and-weather-report.aspx"
terrainAndLiftStatus = "the-mountain/mountain-conditions/terrain-and-lift-status.aspx"

resorts = {
	'Heavenly': heavenly,
	'Kirkwood': kirkwood,
	'Northstar': northstar
}

def getMostRecentReports():
	# Headless seems to crash in ubuntu so will test in the live env with headless.
	options = Options()
	# options.headless = True
	path = os.getcwd()+"/src/geckodriver/geckodriver"
	driver = webdriver.Firefox(options=options, executable_path=path)

	reports = {}

	for resort in resorts:
		page = ""
		failure = False

		# Tries to get snow info
		try:
			page = getPage(driver, resorts[resort]+snowAndWeatherReports)
			thisReport = parseSnowPage(page, resort)
		except Exception as e:
			failure = True
			page = ""
			raise e

		# Tries to get terrain and lift status
		try:
			page = getPage(driver, resorts[resort]+terrainAndLiftStatus)
			thisReport.update(parseLiftPage(page, resort))
		except Exception as e:
			failure = True
			page = ""
			raise e

		if not failure:
			reports[resort] = (thisReport)

	# print("Reports returned:")
	# print(reports)
	driver.close()
	return reports

def getPage(driver, site):
	driver.get(site)
	return driver.page_source

def parseSnowPage(page, resort):
	report = {
		"resort": resort,
		"day": None,
		"two_day": None,
		"seven_day": None,
		"snow_depth": None,
		"season_total": None,
		"last_updated_date": str(date.today()),
		"last_updated_time": datetime.now().strftime("%H:%M"),
		"units": "in.",
	}

	# Parse page with bs4
	soup = BeautifulSoup(page, 'html.parser')
	snowMeasurements = soup.findAll("h5", {"class": "snow_report__metrics__measurement c78__total1--v1"})

	# Get info from each section
	if report["resort"] != "Heavenly":
		try:
			report["day"] = int((snowMeasurements[1].get_text().split("in")[0]))
			report["two_day"] = int((snowMeasurements[2].get_text().split("in")[0]))
			report["seven_day"] = int((snowMeasurements[3].get_text().split("in")[0]))
			report["snow_depth"] = int((snowMeasurements[4].get_text().split("in")[0]))
			report["season_total"] = int((snowMeasurements[5].get_text().split("in")[0]))
		except Exception as e:
			print("Fricking selenium!@!?!?!>!@ FdSAfDSFas lkfjs")
			raise 
	else:
		try:
			report["day"] = int((snowMeasurements[0].get_text().split("in")[0]))
			report["two_day"] = int((snowMeasurements[1].get_text().split("in")[0]))
			report["seven_day"] = int((snowMeasurements[2].get_text().split("in")[0]))
			report["snow_depth"] = int((snowMeasurements[3].get_text().split("in")[0]))
			report["season_total"] = int((snowMeasurements[4].get_text().split("in")[0]))
		except Exception as e:
			print("Fricking selenium!@!?!?!>!@ FdSAfDSFas lkfjs")
			raise e
	return report

def parseLiftPage(page, resort):
	report = {
		"resort": resort,
		"open_acres": None,
		"lifts_open": None,
	}

	# Parse page with bs4
	soup = BeautifulSoup(page, 'html.parser')
	liftTerrainStatus = soup.findAll("span", {"class": "c118__number1--v1"})

	# Get terrain and lift information
	if report["resort"] == "Kirkwood":
		report["open_acres"] = 2300
		report["lifts_open"] = 10
	else:
		try:
			report["open_acres"] = int(liftTerrainStatus[0].get_text().replace(",",""))
			report["lifts_open"] = int(liftTerrainStatus[1].get_text().replace(",",""))
		except Exception as e:
			print("Lift and terrain failed :'(")
			raise e
	return report

if __name__ == '__main__':
	getMostRecentReports()