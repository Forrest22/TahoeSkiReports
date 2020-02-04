from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path="geckodriver-v0.26.0-linux64/geckodriver")
driver.get('https://www.snow.com/mountainconditions/snowandweatherreports.aspx')

soup = BeautifulSoup(driver.page_source, 'html.parser')

# soup.find('table')
# soup = BeautifulSoup(url_get.content, 'html.parser')
# The following is dependant on the "lmxl" library
# soup = BeautifulSoup(url_get.content, 'lmxl')

# print(soup.prettify())
print(soup.findAll("h1", {"class": "hero__content__title reverse"}))
# print(soup.findAll("ul", {"class": "snow_report__metrics col-xs-12"}))
print(soup.findAll("h5", {"class": "snow_report__metrics__measurement c78__total1--v1"}))

#snow_report_1 > div.snow_report__content.row > ul > li:nth-child(7) > div > h5