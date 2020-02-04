from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from bs4 import BeautifulSoup
import os

chrome_options = Options()  
chrome_options.add_argument('--headless')

if os.name == 'nt':
	driver = webdriver.Chrome(executable_path='chromedriver.exe')

driver.get('https://www.snow.com/mountainconditions/snowandweatherreports.aspx')

soup = BeautifulSoup(driver.page_source, 'html.parser')

# soup.find('table')
# soup = BeautifulSoup(url_get.content, 'html.parser')
# The following is dependant on the "lmxl" library
# soup = BeautifulSoup(url_get.content, 'lmxl')



# print(soup.prettify())
print(soup.findAll("ul", {"class": "snow_report__metrics col-xs-12"}))
print(soup.findAll("h5", {"class": "snow_report__metrics__measurement c78__total1--v1"}))

#snow_report_1 > div.snow_report__content.row > ul > li:nth-child(7) > div > h5