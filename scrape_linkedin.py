from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

########## Variables

#Search terms to find in the posted job qualifications
categories = list()

uname = "your@email.com"
password_val = "**********"

#For simplicity, copy these values from a real search 
geoId=000000000
keywords='python'
location='United%20States'


######## Helper Functions

def saveToFile(input_string):
	f = open("linkedin_results.html", "a")
	f.write(input_string)
	f.close()

def CreateHTML(driver, link, html_string):
	title = driver.find_element_by_tag_name('h1').text
	content = driver.find_element_by_id('job-details').find_elements_by_xpath(".//*")
	content_vals = list()
	for c in content:
		content_vals.append("<" + c.tag_name + ">" + c.text + "</" + c.tag_name + ">")
	html_string += "<h1><a href=" + link + ">" + title + "</a></h1>"
	s = " "
	html_string += s.join(content_vals)
	return html_string


######### Code

if __name__ in "__main__":

	######## Log In
	
	#The webdriver is required
	driver = webdriver.Chrome('/Your/Location/chromedriver')
	driver.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')

	username = driver.find_element_by_id('username')
	username.send_keys(uname)
	sleep(0.5)

	password = driver.find_element_by_id('password')
	password.send_keys(password_val)
	sleep(0.5)

	sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
	sign_in_button.click()
	sleep(0.5)

	######### Find Jobs

	driver.get('https://www.linkedin.com/jobs/search/?geoId={}&keywords={}&location={}'.format(geoId, keywords, location))
	sleep(2)

	linkRefs = driver.find_elements_by_class_name('job-card-search__link-wrapper')
	
	links = dict()
	
	for link in linkRefs:
		links[link.get_attribute('href')] = 1
	
	for link in links:
	#	print(link.get_attribute('href'))
		b = False
		driver.get(link)
		sleep(0.5)
		jobName = driver.find_element_by_tag_name('h1').text
		try:
			driver.find_element_by_css_selector('button[aria-controls="job-details"]').click()
		except:
			driver.find_element_by_class_name('msg-overlay-bubble-header__show-hide').click()
			sleep(0.25)
			driver.find_element_by_css_selector('button[aria-controls="job-details"]').click()
		sleep(0.5)
		requirements = driver.find_elements_by_tag_name('li')
		sleep(0.5)
		#try:
		if True:
			for req in requirements:
				for cat in categories:
					if cat in req.text:
						#print(link + "   " + jobName)
						html_string = ''
						html_string = CreateHTML(driver, link, html_string)
						saveToFile(html_string)
						b = True
						break
					if b:
						break
		#except:
		#	pass
