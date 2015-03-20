import requests
from bs4 import BeautifulSoup
import os.path
import re
def get_property_web_scrapping():
	"""
	this function will send response to the url with 4 page, one after another scrap the description and href from property and returns the dictionary

	Args:

	None

	Returns:

	properties_dict  dictionary where key is href and value is description
	"""
	#dictionary where key is href and value is description
	properties_dict = {}
	for page_no in xrange(1,4):
		link = "http://www.realestate.com.au/buy/between-0-1000000-in-perth+-+greater+region%2c+wa%3b+/list-" + str(page_no) + "?includeSurrounding=false&misc=ex-under-contract&activeSort=list-date&source=location-search"
		try:
			response = requests.get(link)
			if response.ok:
			    soup = BeautifulSoup(response.text)
			    #get all division of every result
			    div_tags = soup.find_all('div',"resultBody")
			    for div_tag in div_tags:
			    	#get href of anchor tag
			    	anchor_tag = div_tag.find_all('a',{"class" : "name", "rel": "listingName"})
			    	#get description of each of the property
			    	description_tag = div_tag.find_all('p',{"class" :"description"})
			    	if len(anchor_tag) == 1 and len(description_tag) == 1:
						anchor_tag = anchor_tag[0]
						description_tag = description_tag[0]
						properties_dict[anchor_tag["href"]] = description_tag.text.encode('utf-8').strip()
			else:
				print "response is not successful"
		except:
			print "exception in getting description"
	return properties_dict

def get_new_str_list_not_in_file(list_values):
	"""
	this function will read file OldPropertyList.txt and returns new values which is not present in the input
	it will first split values in file basedupon , and then subtract it from input and return the result. if the file does not exists when running script first time it will return input.

	Args:

	list_values (List) : list of values

	Returns:

	new values which are not present in OldPropertyList.txt 
	"""
	if os.path.exists("OldPropertyList.txt"):
		with open("OldPropertyList.txt", "r") as fp:
			str_comma_separated = fp.read()
			list_values_from_file = str_comma_separated.split(",")
			return list(set(list_values)-set(list_values_from_file))
	else:
		return list_values

def dump_list_to_file(list_values):
	"""
	this function will write file OldPropertyList.txt with list converted to comma separated string

	Args:

	list_values (List) : list of values

	Returns:

	None
	"""
	with open("OldPropertyList.txt", "w") as fp:
		str_comma_separated = ",".join(map(str,list_values))
		fp.write(str_comma_separated)

def get_property_id(href):
	"""
	this function will be used to get property-id from href
	logic is split is using - and get the last string
	Args:

	href (str) : href of property

	Returns:

	property_id
	"""
	return href.split("-")[-1]
def search_keyword(description):
	"""
	this function will search keyword with regular expression in the description
	logic is split is using - and get the last string
	Args:

	description (str) : string text

	Returns:

	True if any keyword found in the description else False
	"""
	key_words_list = ["ocean view*", "city view*", "island view*", "sunset*", "sun set*", "picturesque*", "panoramic", "elevat*", "renovat*", "handym*n", "handy m*n", "handym*n", "develop*"]
	found = False
	for key_word in key_words_list:
		if re.search(key_word, description):
			found = True
	return found

properties_dict = get_property_web_scrapping()
href_list = get_new_str_list_not_in_file(properties_dict.keys())
for href in href_list:
	description = properties_dict[href]
	if search_keyword(description):
		print description
		#put email funcitonality here
dump_list_to_file(href_list)
