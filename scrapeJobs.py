from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import time
import localcred
import pickle
from tqdm import tqdm
from time import sleep
from urllib.parse import urljoin
import df_to_email
import random



def randomize_move(b):
    random_number = random.randint(800,1200)
    random_number = str(random_number)
    b.execute_script(f"window.scrollTo(10, {random_number})")


# TODO move inputs to functions
# TODO get jobid from URLs
# TODO check for duplicate posting when traversing pages
#TODO add job level detail


def validate_string(prompt):
    while True:
        string_input = input(prompt).replace(" ", "")
        if not string_input.isalpha():
            print("Invalid input. Please enter a string with no numeric values.")
        else:
            return string_input


def get_num_jobs():
    while True:
        try:
            num_of_jobs = input("Enter max number of jobs to get (1-100): ")
            if num_of_jobs.startswith("0") or not num_of_jobs.isnumeric():
                raise ValueError
            num_of_jobs = int(num_of_jobs)
            if num_of_jobs < 1 or num_of_jobs > 100:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 100.")
    return num_of_jobs


def get_distance():
    # 5=8k 10=18k 25=40k 50=80k 100=160
    distances = {8: 5, 18: 10, 40: 25, 80: 50, 160: 100}

    while True:
        try:
            distance_km = input("Enter distance in km (8 - 18 - 40 - 80 - 160): ")
            if distance_km.startswith("0") or not distance_km.isnumeric():
                raise ValueError
            distance_km = int(distance_km)
            if distance_km not in distances:
                raise ValueError
            distance = distances[distance_km]
            break
        except ValueError:
            print("Invalid input. Please enter a valid distance.")

    return distance


def get_sortby_choice():
    # Define list of valid sorting options
    options = [
        "job title",
        "company name",
        "main location",
        "work place type",
        "date posted",
        "skills",
        "distance traveltime",
    ]
    while True:
        sortby_choice = input(f"Sort by? options: {', '.join(options)}\n")
        if sortby_choice in options:
            # clean leadin ending spaces and insert _
            sortby_choice = sortby_choice.strip().replace(" ", "_")
            sortby_choice = sortby_choice.upper()
            # use INT_MIN_DURATION column for this sorting
            if sortby_choice == "DISTANCE_TRAVELTIME":
                sortby_choice = "INT_MIN_DURATION"
            return sortby_choice
        else:
            print("Invalid choice. Please enter a valid sorting option.")


def validate_email(prompt):
    while True:
        email_input = input(prompt)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_input):
            print("Invalid email. Please enter a valid email address.")
        else:
            return email_input


# uncomment for user input
# job_title = validate_string("Enter job title: ")
# job_city = validate_string("Enter city: ")
# job_country = validate_string("Enter job Country: ")
# job_state = validate_string("Enter job State: ")
# receiver_email = validate_email("Enter email address: ")
# num_of_jobs = get_num_jobs()
# distance = get_distance()
#sortby_choice = get_sortby_choice()
# logging_in = input("Log in ? y/n: ")


# fixed variables, comment for user input
job_title = "it"
job_city = "Weinsberg"
job_country = "Germany"
job_state = "baden-Württemberg"
num_of_jobs =95
sortby_choice="INT_MIN_DURATION"
distance=25
email_to = "jesusg714@gmail.com"  # can send to multiple emails
logging_in = "n"
given_origin = "Weinsberg,baden-Württemberg"



# So script wont always log user in and get detected, get cookies



if logging_in == "y":
    browser = webdriver.Chrome()  # start a web browser
    """ Opening linkedIn's login page & Log in """
    randomize_move(browser)
    browser.get("https://linkedin.com/uas/login")
    # waiting for the page to load
    wait = WebDriverWait(browser, 20)
    username = wait.until(EC.visibility_of_element_located((By.NAME, "session_key")))
    username = browser.find_element(By.ID, "username")
    username.send_keys(localcred.u_cred)
    time.sleep(3)
    # submit entries
    pword = browser.find_element(By.ID, "password")
    pword.send_keys(localcred.p_cred)
    time.sleep(3)
    # click the button
    button = browser.find_element(By.XPATH, "//button[text()='Sign in']").click()
    time.sleep(3)
    # steps to login
    pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))
    browser.close()
    """ Logged in Now """

# Calculate num of pages needed to traverse
page = (num_of_jobs - 1) // 25 + 1
# search all pages
job_links = []

# Create a new instance of the Firefox driver
with webdriver.Chrome() as browser:
    browser.get("https://www.linkedin.com")
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)
    browser.refresh()
    time.sleep(2)

    #go to jobs page
    url = f"https://www.linkedin.com/jobs/search/?currentJobId=3501167810&distance={distance}&geoId=107182689&keywords={job_title}&location={job_city}%2C%20{job_state}%2C%20Germany&refresh=true"
    print("outside")
    for page_num in range(1, page + 1):

        print(page_num,page+1)
        browser.get(url)
        # Get the page source using Selenium
        page_source = browser.page_source
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        time.sleep(1)
        # Find the element with the class "jobs-search-results-list"
        element = browser.find_element(By.CLASS_NAME, 'jobs-search-results-list')

        # Scroll the element down by the specified amount
        for i in range(5): # Scroll down 10 times
            browser.execute_script(f"arguments[0].scrollBy(0, {800});",element)
            time.sleep(2)
        time.sleep(4)

        #now that its loaded, grab new loaded content source
        page_source = browser.page_source
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        time.sleep(1)

        # find all elements with the class "full-width artdeco-entity-lockup__title ember-view"
        elements = soup.find_all("div", class_="full-width artdeco-entity-lockup__title ember-view")
        # Loop through each div element and extract the href attribute of the first <a> tag
        for div in elements:
            href = div.find('a').get('href')
            # Convert relative links to absolute links
            absolute_href = urljoin(url, href)
            # Add absolute link to job_links list
            job_links.append(absolute_href)

        print(len(job_links))

        # find the button using its CSS selector
        button = browser.find_element(By.CSS_SELECTOR, f'button[aria-label="Page {str(page_num+1)}"]')
        # click the button
        button.click()
        time.sleep(2)
        url=browser.current_url
        
    # quit()
    # get number of items request (shorten list if necessary)
    job_links = job_links[:num_of_jobs]
    # print(job_links)
    time.sleep(2)
    randomize_move(browser)

    """ Now that we have all links from first page,
        iterate each link and gather information for each """

    tmp = 0
    data = []
    for job in tqdm(job_links):
        randomize_move(browser)
        # tuple contains individual info for each job post
        data_tup = ()
        # get URL
        indv_url = job
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

        company = soup.find(
            "span",
            class_="jobs-unified-top-card__company-name",
        ).text.strip()
        data_tup = data_tup + (company,)

        location = soup.find(
            "span",
            class_="jobs-unified-top-card__bullet",
        ).text.strip()
        data_tup = data_tup + (location,)

        workplace_type = soup.find(
            "span",
            class_="jobs-unified-top-card__workplace-type",
        )
        if workplace_type is not None:
            workplace_type = workplace_type.text.strip()
            data_tup = data_tup + (workplace_type,)
        else:
            data_tup = data_tup + ("No work place info",)

        date_posted = soup.find(
            "span",
            class_="jobs-unified-top-card__posted-date",
        ).text.strip()
        data_tup = data_tup + (date_posted,)

        # Skills: get <ul> that has <li> containing all skills
        ul = soup.find("ul", {"class": "job-details-skill-match-status-list"})
        if ul is not None:
            # now that I have <li> with skills,strip unnecessary chars
            # remove "add" from results
            skills_list = [li.text.strip().replace("Add", "") for li in ul.find_all("li")]
            # remove /n and spaces from results
            cleaned_list = [item.strip() for item in skills_list]
            # create a readable string
            skills_result = ", ".join([item.strip() for item in cleaned_list])
            data_tup = data_tup + (skills_result,)
        else:
            data_tup = data_tup + ("No skills section found.",)

        # retrieve skills macthed
        matched_skills = soup.find("h4", {"class": "t-bold t-16"})
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
        tmp += 1

        if tmp == num_of_jobs:
            break


    browser.quit()

""" Working with Data Frames """

# insert gathered data to data frame
df = pd.DataFrame(data)
# save raw df locally before creating columns
df.to_csv("my_data_raw.csv", index=False)
df = df_to_email.clean_data(df, sortby_choice, given_origin)
df_to_email.send_emails(df, email_to)
