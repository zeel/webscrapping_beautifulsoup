import requests
from bs4 import BeautifulSoup
import os.path
import re
import time
import random
import smtplib
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
        #variable which stores the url of website
        website_url = "http://www.realestate.com.au"
        link = "http://www.realestate.com.au/buy/between-0-1000000-in-perth+-+greater+region%2c+wa%3b+/list-" + str(page_no) + "?includeSurrounding=false&misc=ex-under-contract&activeSort=list-date&source=location-search"
        response_text = get_response_text(link)
        if response_text:
            soup = BeautifulSoup(response_text)
            #get all division of every result
            #div_tags = soup.find_all('div',"resultBody")
            anchor_tags = soup.find_all('a',{"class" : "name", "rel": "listingName"})
            for anchor_tag in anchor_tags:
                #get description of each of the property
                property_page_url = website_url + anchor_tag["href"]
                description_text = get_description(property_page_url) 
                if description_text:
                	properties_dict[anchor_tag["href"]] = description_text
    return properties_dict
def get_response_text(url):
    """
    this function will send response to the url 
    every request will have random sleep time between 5 10 15 seconds
    Args:

    url (str) : url where to send request

    Returns:

    html text of response if successful else None
    """
    response_text = None
    get_sleep_for_random_time()
    headers = {'User-Agent': "Mozilla/5.0 ;Windows NT 6.3; WOW64; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/39.0.2171.95 Safari/537.36 "}
    response = requests.get(url, headers = headers)
    if response.ok:
        response_text = response.text
    else:
        print "response to page " + url +" is not successful"
    return response_text

def get_description(property_page_url):
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
    property_page_response_text = get_response_text(property_page_url)
    if property_page_response_text:
        soup_property_page = BeautifulSoup(property_page_response_text)
        p_tag = soup_property_page.find('p',{"class" : "body"})
        if p_tag:
	        description_text = p_tag.text.encode('utf-8').strip()
	        #this is to remove show more for longer description. it can be that if description is not longer then it will not have show more button
	        #so this part will check first if show more is button there and if it's there it will append the hidden description text.
	        span_tags = p_tag.find_all("span")
	        for span_tag in span_tags:
	            if span_tag.text.encode('utf-8').strip() == "...":
	            	if "data-description" in span_tag.attrs:
		                show_more_description_text = span_tag["data-description"].encode('utf-8').strip()
		                description_text += show_more_description_text
    return description_text

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
    this function will append file OldPropertyList.txt with list converted to comma separated string

    Args:

    list_values (List) : list of values

    Returns:

    None
    """
    data_exists = 0
    if os.path.exists("OldPropertyList.txt"):
        data_exists = 1
    with open("OldPropertyList.txt", "a") as fp:
        str_comma_separated = ",".join(map(str,list_values))
        if data_exists:
            #add comma before the string as data exists in file
            str_comma_separated = "," + str_comma_separated
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
    this function will search keyword with regular expression in the description case-insensitive
    Args:

    description (str) : string text

    Returns:

    True if any keyword found in the description else False
    """
    key_words_list = ["ocean view*", "city view*", "island view*", "sunset*", "sun set*", "picturesque*", "panoramic", "elevat*", "renovat*", "handym*n", "handy m*n", "handym*n", "develop*"]
    found = False
    for key_word in key_words_list:
        if re.search(key_word, description, re.IGNORECASE):
            found = True
    return found
def get_sleep_for_random_time():
    """
    this function will sleep the script for randome time between 5 to 15 seconds.
    Args:

    None

    Returns:

    None
    """
    sleep_time = random.uniform(5, 15)
    time.sleep(sleep_time)

properties_dict = get_property_web_scrapping()
href_list = get_new_str_list_not_in_file(properties_dict.keys())
search_href_successful_list = []
msg = ""
for href in href_list:
    description = properties_dict[href]
    print description
    if search_keyword(description):
        search_href_successful_list = search_href_successful_list + ["http://www.realestate.com.au" + href]
dump_list_to_file(href_list)
msg = "Following are the list of property which are new and whose description have keywords:\n" + "\n".join(search_href_successful_list)
server = smtplib.SMTP('localhost')
server.set_debuglevel(1)
#server.sendmail(from, to, msg)
server.sendmail("zeel.shah@aspiringminds.in", "kshah215@gmail.com", msg)
server.quit()