import requests
from bs4 import BeautifulSoup

job_title = input("Enter job title: ")
job_city= input("Enter city: ")
job_country = "Germany" #input("Enter job location: ")

# Construct the URL based on user inputs
url = f"https://www.linkedin.com/jobs/search/?currentJobId=3456221826&geoId=103035651&keywords={job_title}&location={job_city}%2C%20{job_country}&refresh=true"

# Send a GET request with headers to mimic a web browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
response = requests.get(url, headers=headers)
print(response)

# Parse the HTML response using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Extract job listings from the parsed HTML
job_listings = soup.find_all("li", class_="result-card job-result-card result-card--with-hover-state")

# Print the job listings
for job in job_listings:
    title = job.find("h3", class_="result-card__title job-result-card__title").text.strip()
    company = job.find("a", class_="result-card__subtitle job-result-card__subtitle").text.strip()
    location = job.find("span", class_="job-result-card__location").text.strip()
    date_posted = job.find("time", class_="job-result-card__listdate--new").text.strip()

    print(f"Job Title: {title}")
    print(f"Company: {company}")
    print(f"Location: {location}")
    print(f"Date Posted: {date_posted}")
    print()
