import requests
from bs4 import BeautifulSoup

job_title = input("Enter job title: ")
job_location = input("Enter job location: ")
url = f"https://en.it-jobs.de/jobs?q={job_title.replace(' ', '+')}&l={job_location.replace(' ', '+')}"

'''
added several headers to the requests, including an Accept-Language header, an Accept-Encoding header,
a Referer header, a DNT header, a Connection header, and an Upgrade-Insecure-Requests header.
These headers are commonly used by web browsers, so including them in your requests can help to 
mimic a real user and avoid detection.
'''
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://en.it-jobs.de/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    job_listings = soup.find_all("div", class_="job_listing")
    for job in job_listings:
        title = job.find("h2", class_="job_title").text.strip()
        company = job.find("div", class_="job_company").text.strip()
        location = job.find("span", class_="job_location").text.strip()
        summary = job.find("div", class_="job_description").text.strip()
        print(f"Title: {title}\nCompany: {company}\nLocation: {location}\nSummary: {summary}\n")
else:
    print("Error: Request returned status code", response.status_code)
