from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support import expected_conditions as EC

import requests
from bs4 import BeautifulSoup
import time
import localcred

job_title = input("Enter job title: ")
job_city = input("Enter city: ")
job_country = input("Enter job location: ")

# job_title = "Software developer"
# job_city = "Berlin"
# job_country = "Germany"

browser = webdriver.Chrome()  # start a web browser

""" Opening linkedIn's login page & Log in """
browser.get("https://linkedin.com/uas/login")
# waiting for the page to load
wait = WebDriverWait(browser, 10)
username = wait.until(EC.visibility_of_element_located((By.NAME, "session_key")))
# print(browser.page_source)
username = browser.find_element(By.ID, "username")
username.send_keys(localcred.u_cred)
# submit entries
pword = browser.find_element(By.ID, "password")
pword.send_keys(localcred.p_cred)
# click the button
button = browser.find_element(By.XPATH, "//button[text()='Sign in']").click()
""" Logged in Now """

# Construct the URL based on user inputs
url = f"https://www.linkedin.com/jobs/search/?currentJobId=3456221826&geoId=103035651&keywords={job_title}&location={job_city}%2C%20{job_country}&refresh=true"

# Send a GET request with headers to mimic a web browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
front_page_response = requests.get(url, headers=headers)
# print(response)

# Parse the HTML response using BeautifulSoup , make it nicer so we can search it
soup = BeautifulSoup(front_page_response.content, "html.parser")
# print(soup)

# Extract link listings from the parsed HTML by extracting elements
job_links = soup.find_all(
    "a", class_="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]"
)

# Loop through the list of elements and print the href attribute of each one (get links)
for a in job_links:
    href = a["href"]
    # print(href)

""" Now that we have all links from first page,
    iterate each link and gather information for each """

tmp = 0
for job in job_links:
    # get URL
    indv_url = job["href"]
    print(indv_url)

    """ Navigate to each website and extract data"""
    # retrieve fully rendered HTML content
    time.sleep(5)
    browser.get(indv_url)  # navigate to URL
    # print(indv_url)
    time.sleep(2)

    # To get skills we must click on more button
    button = browser.find_element(
        By.XPATH, "//button[@class='jobs-unified-top-card__job-insight-text-button']"
    ).click()
    time.sleep(1)
    content = browser.page_source
    # print(content)

    soup = BeautifulSoup(content, "html.parser")
    # print(soup)
    # Now that we general content , need to parse for specific details
    title = soup.find(
        "h1",
        class_="t-24 t-bold jobs-unified-top-card__job-title",
    ).text.strip()
    print(title)
    company = soup.find(
        "span",
        class_="jobs-unified-top-card__company-name",
    ).text.strip()
    print(company)
    location = soup.find(
        "span",
        class_="jobs-unified-top-card__bullet",
    ).text.strip()
    print(location)

    workplace_type = soup.find(
        "span",
        class_="jobs-unified-top-card__workplace-type",
    )
    if workplace_type is not None:
        workplace_type = workplace_type.text.strip()
        print(workplace_type)
    date_posted = soup.find(
        "span",
        class_="jobs-unified-top-card__posted-date",
    ).text.strip()
    print(date_posted)

    # SKILLS: get <ul> that has <li> containing all skills
    ul = soup.find("ul", {"class": "job-details-skill-match-status-list"})
    # now that I have <li> with skills,strip unnecessary chars
    # remove "add" from results
    skills_list = [li.text.strip().replace("Add", "") for li in ul.find_all("li")]
    # remove /n and spaces from results
    cleaned_list = [item.strip() for item in skills_list]
    # create a readable string
    result = ", ".join([item.strip() for item in cleaned_list])
    print(result)

    main_details = soup.find(
        "div",
        class_="jobs-box__html-content jobs-description-content__text t-14 t-normal jobs-description-content__text--stretch",
    ).text.strip()
    print(main_details, "\n")

    time.sleep(1)
    tmp += 1  # testing
    if tmp == 2:  # testing
        break
