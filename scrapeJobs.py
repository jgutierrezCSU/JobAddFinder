import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

job_title = input("Enter job title: ")
job_location = input("Enter job location: ")
url = f"https://www.indeed.com/jobs?q={job_title.replace(' ', '+')}&l={job_location.replace(' ', '+')}"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    job_listings = soup.find_all("div", class_="jobsearch-SerpJobCard")
    for job in job_listings:
        title = job.find("a", class_="jobtitle").text.strip()
        company = job.find("span", class_="company").text.strip()
        location = job.find("div", class_="recJobLoc")["data-rc-loc"]
        summary = job.find("div", class_="summary").text.strip()
        print(f"Title: {title}\nCompany: {company}\nLocation: {location}\nSummary: {summary}\n")
else:
    print("Error: Request returned status code", response.status_code)
