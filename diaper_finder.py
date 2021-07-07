"""selenium_test.py: This is a test script to check some selenium action on a web form."""


__author__      =      "Abdul Quayum"

from os import getcwd
from sys import platform
import smtplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import traceback
from selenium import webdriver
#from src.testproject.sdk.drivers import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import json
from selenium.webdriver.chrome.options import Options
# from send_email import send_email_with_attachments


def select_chromedriver():
	global chrome_driver_path
	if platform == "linux" or platform == "linux2":
		chrome_driver_path = getcwd() + '/chromedriver_linux'
	elif platform == "darwin":
		chrome_driver_path = getcwd() + '/chromedriver_mac'
	elif platform == "win32":
		chrome_driver_path = getcwd() + '/chromedriver.exe'

chrome_driver_path = ''
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
# options.add_argument("window-size=1400,600")
select_chromedriver()
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
# driver = webdriver.Chrome()
url = 'https://www.amazon.ca/'

# ASSIGINING XPATH VALUE FOR ALL THE FIELDS
top_search_box = "//input[@id='twotabsearchtextbox']"
top_search_button = "//input[@id='nav-search-submit-button']"
per_count_element = "//span[@class='a-size-base a-color-secondary']"
filter_0_to_3m = "//li[@ aria-label='Birth to 3 Months']//a"
filter_4_to_7m = "//li[@ aria-label='4 to 7 Months']//a"
filter_8_to_11m = "//li[@ aria-label='8 to 11 Months']//a"
filter_12_to_23m = "//li[@ aria-label='12 to 23 Months']//a"
filter_24_and_up = "//li[@ aria-label='24 Months & Up']//a"
pagination_next = "//ul[@class='a-pagination']//a[text()='Next']"

# WALMART XPATHS
w_topsearch_box = "//input[@data-automation='search-form-input']"
w_topsearch_button = "//button[@data-automation='search-form-submit']"
w_open_filter_size = "//label[text()='Size']//..//..//*[local-name() = 'svg']"
w_filter_size1 = "//span[text()='Size 1']//..//..//..//..//..//input[@type='checkbox']"
# w_filter_toddler = "//span[text()='Toddler']//..//..//..//..//..//input[@type='checkbox']"
# w_filter_infant = "//span[text()='Infant']//..//..//..//..//..//input[@type='checkbox']"
w_price_per_unit = "//span[@data-automation='price-per-unit']/span/span"

w_endofpage = "//a[text()='Copyright © Walmart 2021']"

per_price_list = []
per_price_link_list = []



def exception_to_string(excep):
	stack = traceback.extract_stack()[:-3] + traceback.extract_tb(excep.__traceback__)
	pretty = traceback.format_list(stack)
	return ''.join(pretty) + '\n {} {}'.format(excep.__class__,excep)

def get_config_value(key):
	value = ''
	try:
		f = open('config', 'r')
		data = f.read()
		data = json.loads(data)
		value = data[key]
	except:
		print('ERROR: config value for ' + key + ' not found.')
	return value

def send_email_with_attachments(subject, body):
	fromaddr = get_config_value('from_email')
	toaddr = get_config_value('subscribe_list')
	login_secret = get_config_value('gmail_access_token')
	# toaddr = "zafi005@gmail.com"

	msg = MIMEMultipart()

	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = subject

	msg.attach(MIMEText(body, 'plain'))

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, login_secret)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	return True

def wait_for_element_and_retrun(elem_xpath, wait_time=10):
	'''
	WAIT FOR A GIVEN TIME (DEFAULT VALUE IS 10 SEC) FOR A GIVEN XPATH AND IF FOUND RETURN THE ELEMENT
	:RETURN TYPE: WEBDRIVER ELEMENT
	'''
	element = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, elem_xpath)), message='ERROR! Element with xpath: "' + elem_xpath + '" not found within ' + str(wait_time) + ' seconds.')
	return element

def wait_for_element_tobe_clickable_and_retrun(elem_xpath, wait_time=10):
	'''
	WAIT FOR A GIVEN TIME (DEFAULT VALUE IS 10 SEC) FOR A GIVEN XPATH AND IF CLICKABLE RETURN THE ELEMENT
	:RETURN TYPE: WEBDRIVER ELEMENT
	'''
	element = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.XPATH, elem_xpath)), message='ERROR! Element with xpath: "' + elem_xpath + '" is not clickable within ' + str(wait_time) + ' seconds.')
	return element

def go_to_page(url, page_title):
	driver.get(url)
	try:
		assert driver.title == page_title	# CHECKING PAGE TITLE IS AS EXPECTED, NOT FAILING TEST CASE AT THIS POINT. JUST GIVING A WARNING.
	except Exception as e:
		print(e)
		print('WARNING! PAGE TITLE NOT FOUND AS EXPECTED. MIGHT FAIL TEST CASE.')

def search_item(search_keyword):
	'''
	THIS METHOD WILL SEARCH USING THE PROVIDED SEARCH KEYWORD AT THE TOP SEARCH BAR.
	'''
	search_box = wait_for_element_and_retrun(top_search_box)
	search_box.send_keys(search_keyword)
	search_button = wait_for_element_tobe_clickable_and_retrun(top_search_button)
	search_button.click()
	sleep(2)
	# driver.save_screenshot("search_result.png")

def add_any_age_filter(index):
	if index == '1':
		filter = wait_for_element_tobe_clickable_and_retrun(filter_0_to_3m)
		filter.click()
		sleep(2)
	elif index == '2':
		filter = wait_for_element_tobe_clickable_and_retrun(filter_4_to_7m)
		filter.click()
		sleep(2)
	elif index == '3':
		filter = wait_for_element_tobe_clickable_and_retrun(filter_8_to_11m)
		filter.click()
		sleep(2)
	elif index == '4':
		filter = wait_for_element_tobe_clickable_and_retrun(filter_12_to_23m)
		filter.click()
		sleep(2)
	elif index == '5':
		filter = wait_for_element_tobe_clickable_and_retrun(filter_24_and_up)
		filter.click()
		sleep(2)
	else:
		print('WARNING: ' + index + ' is not a valid filter option.')

def add_all_age_filters(age_filters):
	if not age_filters:
		return
	try:
		age_filters = age_filters.split(',')
		for i in age_filters:
			add_any_age_filter(i)
	except Exception as e:
		print('WARNING: Invalid filter option provided. Will continue without filter.')

def page_navigation():
	pagination_next_button = wait_for_element_tobe_clickable_and_retrun(pagination_next)
	driver.execute_script("arguments[0].scrollIntoView();", pagination_next_button)
	pagination_next_button.click()
	sleep(2)

def get_all_price_list():
	all_per_price_elem = []
	
	global per_price_list
	global per_price_link_list
	try:
		all_per_price_elem = driver.find_elements_by_xpath(per_count_element)
	except Exception as e:
		print('Error! unable to get price list.')
		print(e)
	if all_per_price_elem:
		c = 0
		for i in all_per_price_elem:
			# getting link
			c = c+1
			per_price_link_path = "(//span[@class='a-size-base a-color-secondary'])[" + str(c) +"]//..//..//a"
			per_price_link_elem = driver.find_element_by_xpath(per_price_link_path)
			per_price_link = per_price_link_elem.get_attribute('href')

			# getting descrition
			item_title_path = "((//span[@class='a-size-base a-color-secondary'])[" + str(c) + "]//..//..//a//..//..//..//span)[1]"
			item_title_elem = driver.find_element_by_xpath(item_title_path)
			item_title = item_title_elem.text

			per_price = i.text
			if '/count' in per_price and 'diaper' in item_title.lower():
				per_price_value = per_price.replace('($', '').replace('/count)', '')
				per_price_list.append(float(per_price_value))

				per_price_link_list.append(per_price_link)
				

def make_link_price_dict():
	link_price_dict = {}
	if len(per_price_link_list) != len(per_price_list):
		print('ERROR! Price and Link lists does not have same content.')
		print(per_price_link_list)
		print(per_price_list)
		return
	for i in range(len(per_price_list)):
		key = str(per_price_list[i])
		value = per_price_link_list[i]
		link_price_dict[key] = value
		# print(per_price_link_list)
		# print(per_price_list)
	return link_price_dict

def save_dict_to_json(dict, file_name='diaper_list.json'):
	f = open(file_name, "w")
	f.write("{\n")
	for k in dict.keys():
		f.write('"{}": "{}",\n\t'.format(k, dict[k]))
	f.write("}")
	f.close()

# def get_subscribers():
# 	subs = ''
# 	get_config_value('subscribe_list')
# 	try:
# 		f = open('config', 'r')
# 		data = f.read()
# 		data = json.loads(data)
# 		subs = data['subscribe_list']
# 	except Exception as e:
# 		print('ERROR: Unable to get subscribers list.')
# 		print(e)
# 	return subs

def run(age_filters='', list_of_pages='5'):
	try:
		go_to_page(url, 'Amazon.ca: Low Prices – Fast Shipping – Millions of Items')
		driver.set_window_size(3840, 2160)
		search_item('diapers')
		add_all_age_filters(age_filters)
		get_all_price_list()
		
		for i in range(int(list_of_pages)-1):
			print('Nevigating to page ' + str(i+2))
			try:
				page_navigation()
				get_all_price_list()
			except:
				print('ERROR! Unable to navigate to page ' + str(i+2))
				break

		# making dict
		link_price_dict = make_link_price_dict()
		# print(link_price_dict)
		global per_price_list
		per_price_list = sorted(per_price_list)
		print('----------')
		print('LOWEST PRICE FOUND: ' + str(per_price_list[0]))
		print('LOWEST PRICE link: ' + str(link_price_dict[str(per_price_list[0])]))

		driver.quit()
		od_link_price_dict = dict(sorted(link_price_dict.items()))
		save_dict_to_json(od_link_price_dict)
		return od_link_price_dict, str(per_price_list[0])
		
		# json.dump(link_price_dict, open( "diaper_list.json", 'w' ) )
	except Exception as e:
		print(exception_to_string(e))
		driver.save_screenshot("fail_result.png")
		driver.quit()

def run_interactive():
	age_filters = str(input("Select an age filter from below (for multiple selection, enter values with comma. e.g. 1,2,3 or Press ENTER for no filter):\n1: For Birth to 3 Months\n2: For 4 to 7 Months \n3: For 8 to 11 Months\n4: For 12 to 23 Months\n5: For 24 Months & Up:\n>")).strip().replace(' ', '')
	list_of_pages = str(input("Enter how many pages you want to search for (Press ENTER to use default 5 pages): >")).strip(). replace(' ', '')
	try:
		list_of_pages = str(int(list_of_pages))
	except:
		print('WARNING: list_of_pages value provided is invalid, will use default value 5.')
		list_of_pages = '5'
	print('Please wait while we are fetching the lowest diaper price from Amazon.ca...')
	run(age_filters, list_of_pages)

def run_default():
	age_filters = '1,2'
	list_of_pages = '5'
	od_dict, lowest_price = run(age_filters, list_of_pages)
	od_dict = json.dumps(od_dict)
	print('Sending email with lowest diaper price list.')
	subject = 'Amazon Diaper lowest price is: ' + lowest_price
	send_email_with_attachments(subject, body=od_dict)
	print('Email sent.')


# # for interactive one
# while True:
# 	run_interactive()

# for default run
run_default()

