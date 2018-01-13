from selenium import webdriver
from bs4 import BeautifulSoup
from collections import defaultdict
import time
import json
import urllib
import re
import csv
import sys

driver = webdriver.Chrome()

linkedin_email = ""
linkedin_password = ""

with open('jquery-3.2.1.min.js', 'r') as jquery_js: 
	jquery = jquery_js.read() 
	driver.execute_script(jquery) #inject jquery into selenium driver

def linkedin_login(email = linkedin_email, password = linkedin_password):
	driver.get('https://www.linkedin.com/nhome')
	driver.find_elements_by_xpath("//input[@name='session_key']")[0].send_keys(email)
	driver.find_elements_by_xpath("//input[@name='session_password']")[0].send_keys(password)
	driver.find_element_by_id("login-submit").click()
	time.sleep(4)
	print("Login successful")

def get_employee_details_url(company):
	search_base_url = "https://www.linkedin.com/ta/federator"
	params = {'orig': 'GLHD',
			  'verticalSelector': 'all',
			  'query': company}
	search_url = "{}?{}".format(search_base_url, urllib.parse.urlencode(params))
	driver.get(search_url)

	# parse results of query
	soup = BeautifulSoup(driver.page_source)
	data = json.loads(soup.find("pre").text)

	company_object = next((item for item in data['resultList'] if item['sourceID'] == 'company'), None)
	if company_object and company_object['id']:
		employee_details_url = "https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%22{}%22%5D".format(company_object['id'])
	else:
		print("Couldn't find company {} in linkedin search results".format(company))
		return

	return employee_details_url

def scrape_employee_details(company_name, company_details_url):
	if not company_details_url:
		return None

	driver.get(company_details_url)

	# Estimate for number of employees
	num_search_results = driver.execute_script("return $('h3.search-results__total')[0]")
	num_employees = re.search("(?<=Showing\s).*(?=\sresults)", num_search_results.text).group(0)
	print('Num employees: '+num_employees)

	# Query employee past companies 
	past_companies = []
	companies = driver.execute_script("return $('li.search-facet.search-facet--past-company').find('input.medium-input')")
	print('\nPast companies:')
	for company in companies:
		print(company.get_attribute('name'))
		past_companies.append(company.get_attribute('name'))

	# Query employee schools
	past_schools = []
	schools = driver.execute_script("return $('li.search-facet.search-facet--school').find('input.medium-input')")
	print('\nPast schools:')
	for school in schools:
		print(school.get_attribute('name'))
		past_schools.append(school.get_attribute('name'))

	# Return results as dict
	return {
		'Company Name': company_name,
		'Num Employees': num_employees,
		'Past Companies': ", ".join(past_companies),
		'Past Schools': ", ".join(past_schools)
	}

# Login to Linkedin
linkedin_login()

with open('company_details.csv', 'a') as f:
	fieldnames = ['company_name', 'num_employees', 'past_companies', 'past_schools']
	writer = csv.DictWriter(f, fieldnames)

	companies = defaultdict(list) 
	with open('companies.csv') as companies_file: # Import company list from csv
		reader = csv.DictReader(companies_file)
		for row in reader: 
			for (k, v) in row.items():
				companies[k].append(v)	
		companies = companies['Company Name']
		for company in companies:
			print('\nReading company: '+company)
			company_url = get_employee_details_url(company)
			talent_dict = scrape_employee_details(company, company_url)
			if not talent_dict:
				continue
			writer.writerow(talent_dict)
			time.sleep(3)

time.sleep(3)
driver.close()
