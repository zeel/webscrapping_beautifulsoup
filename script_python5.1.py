import requests
from bs4 import BeautifulSoup
import os.path
import re
import time
import random
import smtplib
class WebCrawler:
	#list of keyword to be matched in description. + Elevated, "developer", "development",
	regex_key_words_list = ["panoramic", "handym.n", "handy.m.n", "sunset", "(?i)sun[^,.]{0,3}set", "(?i)ocean[^,.]{0,3}view", "(?i)view[^,.]{0,25}ocean", "(?i)sea[^,.]{0,3}view", "(?i)view[^,.]{0,25}sea", "(?i)city[^,.]{0,3}view", "(?i)view[^,.]{0,25}city", "(?i)island[^,.]{0,3}view", "(?i)view[^,.]{0,25}island", "(?i)hill[^,.]{0,3}view", "(?i)view[^,.]{0,25}hill", "(?i)hillside[^,.]{0,3}view", "(?i)view[^,.]{0,25}hillside", "(?i)amazing[^,.]{0,3}view", "(?i)astonishing[^,.]{0,3}view", "(?i)astounding[^,.]{0,3}view", "(?i)astonishing[^,.]{0,3}view", "(?i)breathtaking[^,.]{0,3}view", "(?i)daring[^,.]{0,3}view", "(?i)picturesque[^,.]{0,3}view", "(?i)dazzling[^,.]{0,3}view", "(?i)dramatic[^,.]{0,3}view", "(?i)spectacular[^,.]{0,3}view", "(?i)fabulous[^,.]{0,3}view", "(?i)fantastic[^,.]{0,3}view", "(?i)magnificent[^,.]{0,3}view", "(?i)miraculous[^,.]{0,3}view", "(?i)remarkable[^,.]{0,3}view", "(?i)sensational[^,.]{0,3}view", "(?i)splendid[^,.]{0,3}view", "(?i)striking[^,.]{0,3}view", "(?i)stunning[^,.]{0,3}view", "(?i)thrilling[^,.]{0,3}view", "(?i)wonderful[^,.]{0,3}view", "(?i)wondrous[^,.]{0,3}view", "(?i)staggering[^,.]{0,3}view", "(?i)brilliant[^,.]{0,3}view", "(?i)excellent[^,.]{0,3}view", "(?i)gorgeous[^,.]{0,3}view", "(?i)lavish[^,.]{0,3}view", "(?i)lofty[^,.]{0,3}view", "(?i)noble[^,.]{0,3}view", "(?i)opulent[^,.]{0,3}view", "(?i)outstanding[^,.]{0,3}view", "(?i)palatial[^,.]{0,3}view", "(?i)superb[^,.]{0,3}view", "(?i)luxurious[^,.]{0,3}view", "(?i)rich[^,.]{0,3}view", "(?i)royal[^,.]{0,3}view", "(?i)superior[^,.]{0,3}view", "(?i)transcendent[^,.]{0,3}view", "(?i)vivid[^,.]{0,3}view", "(?i)exceptional[^,.]{0,3}view", "(?i)exquisite[^,.]{0,3}view", "(?i)stately[^,.]{0,3}view", "(?i)delightful[^,.]{0,3}view", "(?i)great[^,.]{0,3}view", "(?i)glorious[^,.]{0,3}view", "(?i)impressive[^,.]{0,3}view", "(?i)opulent[^,.]{0,3}view", "(?i)sublime[^,.]{0,3}view", "(?i)pleasing[^,.]{0,3}view", "(?i)dream[^,.]{0,3}view", "(?i)lovely[^,.]{0,3}view", "(?i)elegant[^,.]{0,3}view", "(?i)marvellous[^,.]{0,3}view", "(?i)grand[^,.]{0,3}view", "(?i)grand[^,.]{0,3}view", "(?i)grandiose[^,.]{0,3}view", "(?i)monumental[^,.]{0,3}view", "(?i)refined[^,.]{0,3}view", "(?i)dignifying[^,.]{0,3}view", "(?i)regal[^,.]{0,3}view", "(?i)fine[^,.]{0,3}view", "(?i)finest[^,.]{0,3}view", "(?i)admirable[^,.]{0,3}view", "(?i)first-rate[^,.]{0,3}view", "(?i)first rate[^,.]{0,3}view", "(?i)first-class[^,.]{0,3}view", "(?i)first class[^,.]{0,3}view", "(?i)beautiful[^,.]{0,3}view", "(?i)enjoyable[^,.]{0,3}view", "(?i)eye-catching[^,.]{0,3}view", "(?i)eye catching[^,.]{0,3}view", "(?i)super[^,.]{0,3}view", "(?i)port[^,.]{0,3}view", "(?i)quintessential[^,.]{0,3}view", "(?i)superlative[^,.]{0,3}view", "(?i)unobstructed[^,.]{0,3}view", "(?i)view[^,.]{0,25}unobstructed"]
	min_sleep_time = 5 #number of seconds
	max_sleep_time = 15 #number of seconds
	#configuration for sending emails
	#set https://www.google.com/settings/security/lesssecureapps to "Turn on"
	#Go to https://g.co/allowaccess from a different device you have previously used to access your Google account 
	GMAIL_USERNAME = "xxx@gmail.com"
	GMAIL_PASSWORD = "xxx"
	recipient = "xxx@gmail"
	email_subject = "property listing"
	properties_visited_dump_file_name = "OldPropertyList.txt"
	properties_with_keywords_dump_file_name = "FoundProperties.html"
	def __init__(self):
		property_not_to_visit_list = self.get_property_not_to_visit()
		self.fetch_description_check_keyword_property(property_not_to_visit_list)
		print("Script has completed it's work")
		#self.sendmail_gmail("script has completed it's work")
	def fetch_description_check_keyword_property(self, property_not_to_visit_list):
		#this variable is boolean flag which will check if the next page is accessible/exists or not
		#if the current page have nextLink class defined in <li> then next page is accessible
		next_page_accessible = True
		page_no = 53
		while next_page_accessible:
			#variable which stores the url of website
			website_url = "http://www.realestate.com.au"		
			link = "http://www.realestate.com.au/buy/property-unitblock-rural-acreage-land-villa-townhouse-house-between-0-1000000-in-fremantle%2c+wa+6160%3b+east+fremantle%2c+wa+6158%3b+bicton%2c+wa+6157%3b+attadale%2c+wa+6156%3b+applecross%2c+wa+6153%3b+ardross%2c+wa+6153%3b+mount+pleasant%2c+wa+6153%3b+alfred+cove%2c+wa+6154%3b+white+gum+valley%2c+wa+6162%3b+south+fremantle%2c+wa+6162%3b+beaconsfield%2c+wa+6162%3b+north+coogee%2c+wa+6163%3b+hamilton+hill%2c+wa+6163%3b+spearwood%2c+wa+6163%3b+coogee%2c+wa+6166%3b+munster%2c+wa+6166%3b+beeliar%2c+wa+6164%3b+henderson%2c+wa+6166%3b+salter+point%2c+wa+6152%3b+como%2c+wa+6152%3b+south+perth%2c+wa+6151%3b+burswood%2c+wa+6100%3b+east+perth%2c+wa+6004%3b+perth%2c+wa+6000%3b+west+perth%2c+wa+6005%3b+highgate%2c+wa+6003%3b+mount+lawley%2c+wa+6050%3b+maylands%2c+wa+6051%3b+north+perth%2c+wa+6006%3b+crawley%2c+wa+6009%3b+dalkeith%2c+wa+6009%3b+nedlands%2c+wa+6009%3b+claremont%2c+wa+6010%3b+swanbourne%2c+wa+6010%3b+cottesloe%2c+wa+6011%3b+peppermint+grove%2c+wa+6011%3b+mosman+park%2c+wa+6012%3b+north+fremantle%2c+wa+6159/list-" + str(page_no) + "?includeSurrounding=false&persistIncludeSurrounding=true&misc=ex-under-contract&source=location-search#"
			#print("\n Full link that is being accessed now is: \n "+ link)
			print("\n\n\n\n\n Will now access the page", page_no, "from the paginated list starting at:\n",link)
			response_text = self.get_response_text(link)
			if response_text:
				soup = BeautifulSoup(response_text)
				#logic to check if the next page is accessible or not
				li_next_link = soup.find_all('li',{"class" : "nextLink"})
				print(li_next_link)
				if li_next_link:
					page_no += 1
				else:
					next_page_accessible = False
				##logic to find property anchor tags
				anchor_tags = soup.find_all('a',{"class" : "name", "rel": "listingName"})
				for anchor_tag in anchor_tags:
					#check that property should not be present in OldProperties.txt
					if anchor_tag["href"] not in property_not_to_visit_list:
						#get description of each of the property
						property_page_url = website_url + anchor_tag["href"]
						print(property_page_url)
						#append this property list to file so that next time they will not be visited
						self.set_property_not_to_visit(anchor_tag["href"])
						description_text = self.get_description(property_page_url)
						print(description_text)
						if description_text:
							keywords_found = self.search_keyword(str(description_text))
							if keywords_found:
								str_keywords_found = ",".join(map(str,keywords_found))
								message = str_keywords_found + ": <a href=\"" + property_page_url + "\">" + property_page_url + "</a>" + "<br>"
								#self.sendmail_gmail(message)
								with open(self.properties_with_keywords_dump_file_name, "a") as fp:
									fp.write(message + "\n")
	def get_response_text(self, url):
		"""
		this function will send response to the url 
		every request will have random sleep time between 5 to 15 seconds
		Args:

		url (str) : url where to send request

		Returns:

		html text of response if successful else None
		"""
		response_text = None
		response = self.retry_request(url)
		if response.ok:
			response_text = response.text
		else:
			print("response to page " + url +" is not successful")
		self.get_sleep_for_random_time()
		return response_text

	def retry_request(self, url):
		"""
		this function checks if the url request was successful or not otherwise it retry after some random delay.
		"""
		headers = {'User-Agent': "Mozilla/5.0 ;Windows NT 6.3; WOW64; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/39.0.2171.95 Safari/537.36 "}
		successful = 0
		response = None
		while successful == 0:
			try:
				response = requests.get(url, headers = headers)
				successful = 1
			except Exception:
				print("could not able to fetch url " + url)
				self.get_sleep_for_random_time()
		return response

	def get_description(self, property_page_url):
		"""
		this function will return description of property page .
		it will search p tag with class body and for longer description it will search span which have text ... as content and it will fetch extra description from it's attribute data-description
		and it will return correct description
		Args:

		property_page_url (str) : url of the property page

		Returns:

		description of the property if successful else None
		"""
		description_text = None
		#print("Will fetch the description of selected property")
		property_page_response_text = self.get_response_text(property_page_url)
		if property_page_response_text:
			soup_property_page = BeautifulSoup(property_page_response_text)
			p_tag = soup_property_page.find('p',{"class" : "body"})
			if p_tag:
				description_text = str(p_tag.text.encode('utf-8').strip(), 'utf-8')
				#this is to remove show more for longer description. it can be that if description is not longer then it will not have show more button
				#so this part will check first if show more is button there and if it's there it will append the hidden description text.
				span_tags = p_tag.find_all("span")
				for span_tag in span_tags:
					#print("found span tags in p")
					if str(span_tag.text.encode('utf-8').strip(), 'utf-8') == "...":
						#print("span has text ...")
						if "data-description" in span_tag.attrs:
							#print("span has attribute data-description")
							show_more_description_text = str(span_tag["data-description"].encode('utf-8').strip(), 'utf-8')
							description_text += show_more_description_text
				description_text = description_text.encode('utf-8')
		return description_text

	def get_property_not_to_visit(self):
		"""
		this function will read file properties_visited_dump_file_name and returns list containing ids of property present in the file.

		Returns:

		list of values which are present- already scraped
		"""
		list_values = []
		if os.path.exists(self.properties_visited_dump_file_name):
			with open(self.properties_visited_dump_file_name, "r") as fp:
				str_comma_separated = fp.read()
				list_values = str_comma_separated.split(",")
				#to make them unique
				list_values = list(set(list_values))
		return list_values

	def set_property_not_to_visit(self, value):
		"""
		this function will append value in file properties_visited_dump_file_name 
		so that they will not be scraped next time.
		Args:

		value (str) : href of the property

		Returns:

		None
		"""
		data_exists = 0
		if os.path.exists(self.properties_visited_dump_file_name):
			data_exists = 1
		with open(self.properties_visited_dump_file_name, "a") as fp:
			if data_exists:
				#add comma before the string as data exists in file
				value = "," + value
			fp.write(value)

	def search_keyword(self, description):
		"""
		this function will search list of keywords with regular expression in the description case-insensitive
		Args:

		description (str) : string text

		Returns:

		list with found keywords in the description else empty list
		"""
		found_keywords = []
		for key_word in self.regex_key_words_list:
			if re.search(key_word, description, re.IGNORECASE):
				print("#########################");
				print("found keyword " + key_word)
				print("#########################");
				found_keywords.append(key_word)
		return found_keywords

	def get_sleep_for_random_time(self):
		"""
		this function will sleep the script for random time between min_sleep_time to max_sleep_time seconds.
		"""
		sleep_time = random.uniform(self.min_sleep_time, self.max_sleep_time)
		print("\n Doing nothing for ",sleep_time," seconds.")
		time.sleep(sleep_time)

	def sendmail_gmail(self, message):
		"""
		this function sends email to recipient using gmail smtp server
		"""
		# The below code never changes, though obviously those variables need values.
		session = smtplib.SMTP('smtp.gmail.com', 587)
		session.ehlo()
		session.starttls()
		session.login(self.GMAIL_USERNAME, self.GMAIL_PASSWORD)
		headers = "\r\n".join(["from: " + self.GMAIL_USERNAME,
							   "subject: " + self.email_subject,
							   "to: " + self.recipient,
							   "mime-version: 1.0",
							   "content-type: text/html"])

		# body_of_email can be plaintext or html!					
		content = headers + "\r\n\r\n" + message
		session.sendmail(self.GMAIL_USERNAME, self.recipient, content)
webcrawler_obj = WebCrawler()
