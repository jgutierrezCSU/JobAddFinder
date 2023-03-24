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

import df_to_email


def randomize_move(b):
    b.execute_script("window.scrollTo(10, 900)")


# uncomment for user input
# job_title = input("Enter job title: ")
# job_city = input("Enter city: ")
# job_country = input("Enter job location: ")
# num_of_jobs = input("Enter max number of jobs to get: ")

# email_to=input("Email to send to: ")

# This code takes user input and assigns the appropriate page number based on the range of input. 
num_of_jobs = int(input("Enter max number of jobs to get (1-100): "))

if num_of_jobs < 1 or num_of_jobs > 100:
    print("Invalid input! Please enter a number between 1 and 100.")
else:
    page = (num_of_jobs - 1) // 25 + 1


# 5=8k 10=18k 25=40k 50=80k 100=160
distances = {8: 5, 18: 10, 40: 25, 80: 50, 160: 100}

try:
    distance_km = int(input("Enter distance in km (8 - 18 - 40 - 80 - 160): "))
    if distance_km not in distances:
        raise ValueError
except ValueError:
    print("Invalid input. Please enter a valid distance.")
    distance = 5
else:
    distance = distances[distance_km]

# fixed variables, comment for user input
job_title = "it"
job_city = "Weinsberg"
job_country = "Germany"
job_state = "baden-Württemberg"
#num_of_jobs = 30
email_to = ["jesusg714@gmail.com"]  # can send to multiple emails


# So script wont always log user in and get detected, get cookies
logging_in = input("Log in ? y/n: ")
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
    time.sleep(5)
    # click the button
    button = browser.find_element(By.XPATH, "//button[text()='Sign in']").click()
    time.sleep(5)
    # steps to login
    pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))
    browser.close()
    """ Logged in Now """

browser = webdriver.Chrome()  # start a web browser
browser.get("https://www.linkedin.com")
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    browser.add_cookie(cookie)
browser.refresh()
time.sleep(2)

# search all pages
job_links = []

for page_num in range(1, page+1):
    print("page_num :",page_num)
    randomize_move(browser)
    time.sleep(3)
    # Construct the URL based on user inputs
    #example
    #https://www.linkedin.com/jobs/search/?currentJobId=3501167810&distance=50&geoId=107182689&keywords=it%7D&location=weinsberg%2C%20baden-W%C3%BCrttemberg%2C%20Germany&refresh=true&start=0
    url = f"https://www.linkedin.com/jobs/search/?currentJobId=3501167810&distance={distance}&geoId=107182689&keywords={job_title}&location={job_city}%2C%20{job_state}%2C%20Germany&refresh=true&start={25 * (page_num - 1)}"

    # Send a GET request with headers to mimic a web browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    front_page_response = requests.get(url, headers=headers)

    # Parse the HTML response using BeautifulSoup , make it nicer so we can search it
    soup = BeautifulSoup(front_page_response.content, "html.parser")

    # Extract link listings from the parsed HTML by extracting elements
    job_links.extend(
        soup.find_all(
            "a",
            class_="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]",
        )
    )

print("job_links ",len(job_links))
time.sleep(4.5)
randomize_move(browser)

""" Now that we have all links from first page,
    iterate each link and gather information for each """

tmp = 0
data = []
for job in tqdm(job_links):
# for job in tqdm(job_links):
    print(",,,,,",tmp)
    randomize_move(browser)
    # tuple contains individual info for each job post
    data_tup = ()
    # get URL
    indv_url = job["href"]

    """ Navigate to each website and extract data"""
    browser.get(indv_url)  # navigate to URL
    time.sleep(4)
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
        time.sleep(3)
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
df = df_to_email.clean_data(df)
df_to_email.send_emails(df, email_to)
