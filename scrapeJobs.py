import requests
from bs4 import BeautifulSoup
import time


job_title = "Software developer"  # input("Enter job title: ")
job_city = "Berin"  # input("Enter city: ")
job_country = "Germany"  # input("Enter job location: ")

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
    url = job["href"]
    # print(url)
    # get a general main page response
    job_posts_response = requests.get(url, headers=headers)
    # print(job_posts_response.content)
    # parse that response for searching
    soup = BeautifulSoup(job_posts_response.content, "html.parser")

    # this variable hasall info from main top card ( title , comp name, loc , date posted)

    print(soup)
    # Now that we have all info , need to parse for specific details
    title = soup.find(
        "h1",
        class_="top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title",
    ).text.strip()
    print(title)
    company = soup.find(
        "span",
        class_="jobs-unified-top-card__company-name",
    )
    print(company)
    # location =
    # date_posted =

    time.sleep(2)
    tmp += 1  # testing
    if tmp == 1:  # testing
        break
# job_posts_response = requests.get(ur, headers=headers)
# print(job_posts_response)


# # Print the job listings
# for job in job_listings:
#     title = job.find("h3", class_="result-card__title job-result-card__title").text.strip()
#     company = job.find("a", class_="result-card__subtitle job-result-card__subtitle").text.strip()
#     location = job.find("span", class_="job-result-card__location").text.strip()
#     date_posted = job.find("time", class_="job-result-card__listdate--new").text.strip()

#     print(f"Job Title: {title}")
#     print(f"Company: {company}")
#     print(f"Location: {location}")
#     print(f"Date Posted: {date_posted}")
#     print()
# <span class="jobs-unified-top-card__company-name">
#                   <a href="/company/medwing/life/" id="ember26" class="ember-view t-black t-normal">
#                     MEDWING
#                   </a>
#             </span>
