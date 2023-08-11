from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import pickle
from tqdm import tqdm
from time import sleep
from urllib.parse import urljoin
import user_input_validations as uiv
import df_to_email
import random
import localcred
import re
import json

"""
localcred file needs :
linkedin_uname = ""
linkedin_pword = ""
email_pword = ""
API_KEY=""

"""
#returns list
def load_prev_ids():
     # Load previously scraped job ids from a local file (if available)
    try:
        with open('saved_ids.json', 'r') as file:
            scraped_job_ids = json.load(file)
    except FileNotFoundError:
        scraped_job_ids = []
    return scraped_job_ids


def save_ids_localy(ids_lst):   
    print(ids_lst)
    with open('saved_ids.json', 'w') as f:
        json.dump(ids_lst, f)
    


def randomize_move(browser):
    """
    Scroll the browser window to a random position between 800 and 1200 pixels.
    """
    random_number = random.randint(800, 1200)
    random_number = str(random_number)
    browser.execute_script(f"window.scrollTo(10, {random_number})")

#check if data is save localy, efficiently iterate n populate new data w/ old/new data
# TODO: Get job ID from URLs.
# TODO: Add job level detail.


# uncomment for user input
logging_in = input("Log in ? y/n: ")
print("Enter job title: ")
job_title = uiv.validate_string()
print("Enter city: ")
job_city = uiv.validate_string()
print("Enter job Country: ")
job_country = uiv.validate_string()
print("Enter job State: ")
job_state = uiv.validate_string()
receiver_email = uiv.validate_email("Enter email address: ")
num_of_jobs = uiv.get_num_jobs()
distance = uiv.get_distance()
sortby_choice = uiv.get_sortby_choice()


# fixed variables, comment for user input
# job_title = "it"
# job_city = "Weinsberg"
# job_country = "Germany"
# job_state = "baden-Württemberg"
# num_of_jobs =98
# sortby_choice="INT_MIN_DURATION"
# distance=10
# email_to = "jesusg714@gmail.com"  # can send to multiple emails
# logging_in = "n"
# given_origin = "Weinsberg,baden-Württemberg"


# Configure Chrome options for headless browsing
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set path to chromedriver executable as per your configuration
chromedriver_path = "./chromedriver"

# So script wont always log user in and get detected, get cookies
if logging_in == "y":
    # start a web browser
    browser = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    """ Opening linkedIn's login page & Log in """
    # opening LinkedIn's login page and logging in
    randomize_move(browser)
    browser.get("https://linkedin.com/uas/login")

    # waiting for the page to load
    wait = WebDriverWait(browser, 20)

    # find username field and enter credentials
    username = wait.until(EC.visibility_of_element_located((By.NAME, "session_key")))
    username.send_keys(localcred.linkedin_uname)
    time.sleep(3)

    # find password field and enter credentials
    pword = browser.find_element(By.ID, "password")
    pword.send_keys(localcred.linkedin_pword)
    time.sleep(3)

    # click the login button
    button = browser.find_element(By.XPATH, "//button[text()='Sign in']").click()
    time.sleep(3)

    # save login session cookies
    pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))

    # close the browser
    browser.close()

# indicate that the user is logged in
""" Logged in Now """


# Calculate num of pages needed to traverse
page = (num_of_jobs - 1) // 25 + 1

job_links = []
# Create a new instance of the Chrome driver
with webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options) as browser:
    browser.get("https://www.linkedin.com")
    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
        browser.refresh()
    except FileNotFoundError:
        print("No cookies found, run script with 'y' option in log in prompt ?")
        quit()
    time.sleep(2)

    # go to jobs page
    #TODO need to get JobID automatically (keeps changing , leads to  no such element: Unable to locate element: {"method":"css selector","selector":".jobs-search-results-list"})
    url = f"https://www.linkedin.com/jobs/search/?currentJobId=3421651472&distance={distance}&geoId=107182689&keywords={job_title}&location={job_city}%2C%20{job_state}%2C%20Germany&refresh=true"
    for page_num in range(1, page + 1):
        browser.get(url)
        # Get the page source using Selenium
        page_source = browser.page_source
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")
        time.sleep(1)
        # Find the element with the class "jobs-search-results-list"
        element = browser.find_element(By.CLASS_NAME, "jobs-search-results-list")

        # Scroll the element down by the specified amount (to load all jobs)
        for i in range(5):  # Scroll down 4 times
            browser.execute_script(f"arguments[0].scrollBy(0, {800});", element)
            time.sleep(2)
        time.sleep(3)

        # now that its loaded, grab new loaded content source
        page_source = browser.page_source
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")
        time.sleep(1)

        # find all elements with the class "full-width artdeco-entity-lockup__title ember-view"
        elements = soup.find_all(
            "div", class_="full-width artdeco-entity-lockup__title ember-view"
        )
        # Loop through each div element and extract the href attribute of the first <a> tag
        for div in elements:
            href = div.find("a").get("href")
            # Convert relative links to absolute links
            absolute_href = urljoin(url, href)
            # Add absolute link to job_links list
            job_links.append(absolute_href)

        # find the button using its CSS selector
        button = browser.find_element(
            By.CSS_SELECTOR, f'button[aria-label="Page {str(page_num+1)}"]'
        )
        # click the button
        button.click()
        time.sleep(2)
        url = browser.current_url

    # get number of items request (shorten list if necessary)
    #job_links = job_links[:num_of_jobs]
    # print(job_links)
    time.sleep(2)
    randomize_move(browser)

    prev_ids=load_prev_ids()
    
    """ Now that we have all links from pages,
        iterate each link and gather information for each """

    tmp = 0
    data = []
    to_prev_ids_lst=[]
    for cur_job in tqdm(job_links):
        #
        cur_job_id=re.search(r"/(\d+)/", cur_job).group(1)
        # print("cur:",cur_job_id,"prev" ,prev_ids)
        if cur_job_id not in prev_ids:           
            randomize_move(browser)
            # print("adding to list")
            # tuple contains individual info for each job post
            data_tup = ()
            # get URL
            indv_url = cur_job
            """ Navigate to each website and extract data"""
            browser.get(indv_url)  # navigate to URL
            time.sleep(2)
            # press button to display Skills section
            # Some profile have or dont have this section, test here
            try:
                wait = WebDriverWait(browser, 8)
                button = wait.until(
                    EC.visibility_of_element_located(
                        (By.CLASS_NAME, "jobs-unified-top-card__job-insight-text-button")
                    )
                )
                button = browser.find_element(
                    By.XPATH,
                    "//button[@class='jobs-unified-top-card__job-insight-text-button']",
                ).click()
                time.sleep(2)
            except:
                pass

            content = browser.page_source
            time.sleep(2)
            soup = BeautifulSoup(content, "html.parser")
            # Now that we general content , need to parse for specific details
            title = soup.find(
                "h1",
                class_="t-24 t-bold jobs-unified-top-card__job-title",
            ).text.strip()
            data_tup = data_tup + (title,)
            '''             '''
            primary_description = soup.find('div', class_='jobs-unified-top-card__primary-description')
            texts = primary_description.find_all(text=True)
            #separate string by , per each index
            text_content = [text.strip() for text in texts if text.strip()]
            text_content = [substring for string in text_content for substring in string.split(', ')]
            print(text_content)
            #get info from indexes
            company =text_content[0]
            location=text_content[1]
            date_posted= text_content[3]
            workplace_type=text_content[5]
            #append to data tuple
            data_tup = data_tup + (company,)
            data_tup = data_tup + (location,)
            data_tup = data_tup + (date_posted,)
            data_tup = data_tup + (workplace_type,)
            
            # Skills: get <ul> that has <li> containing all skills
            ul = soup.find("ul", {"class": "job-details-skill-match-status-list"})
            if ul is not None:
                # now that I have <li> with skills,strip unnecessary chars
                # remove "add" from results
                skills_list = [
                    li.text.strip().replace("Add", "") for li in ul.find_all("li")
                ]
                # remove /n and spaces from results
                cleaned_list = [item.strip() for item in skills_list]
                # create a readable string
                skills_result = ", ".join([item.strip() for item in cleaned_list])
                data_tup = data_tup + (skills_result,)
            else:
                data_tup = data_tup + ("No skills section found.",)

            # retrieve skills macthed\
            matched_skills = soup.find("h2", {"class": "t-bold t-16"})
            if matched_skills is not None:
                matched_skills = matched_skills.text.strip()
                data_tup = data_tup + (matched_skills,)
            else:
                data_tup = data_tup + ("No matched skills",)

            main_details = soup.find(
                "div",
                class_="jobs-box__html-content jobs-description-content__text t-14 t-normal jobs-description-content__text--stretch",
            ).text.strip()

            # clean \n
            main_details = main_details.strip()
            data_tup = data_tup + (main_details,)
            # add link at last column
            data_tup = data_tup + (indv_url,)

            randomize_move(browser)

            # add all data into data frame
            data.append(data_tup)
            time.sleep(2)

            #append new added id to prev ids list
            to_prev_ids_lst.append(cur_job_id)
            tmp += 1
            if tmp == num_of_jobs:
                break
        else:
            print("skipped")
    save_ids_localy(to_prev_ids_lst)
    browser.quit()

""" Working with Data Frames """

# insert gathered data to data frame
df = pd.DataFrame(data)
# save raw df locally before creating columns
df.to_csv("my_data_raw.csv", index=False)
df = df_to_email.clean_data(df, sortby_choice, given_origin)
df_to_email.send_emails(df, email_to)
