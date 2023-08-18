[![Build Status](https://app.travis-ci.com/jgutierrezCSU/WebScrapperPython.svg?branch=master)](https://app.travis-ci.com/jgutierrezCSU/WebScrapperPython)

*Headless* Web scraper for LinkedIn using Python.

Features: <br>
Scrape Jobs using "Job title" , "City" , "State", "Country" and "distance" and optionally, you can use "sort by" and calculate commute time.<br>
Scripts prompts user if they want to manually login (preventing repetitive logins and avoiding detection) <br>
After first log in cookies are saved and no logging in is necessary. <br>  
Script sends an email with the following details after gathering info from site:<br>

<br>

Scraping details include: <br>
Position title <br>
Company name <br>
Main Location <br>
Comute time (user gives origin) <br>
Place of work (could be multiple or remote) <br>
Date posted <br>
Skills needed (if available ) <br>
Number of matched skilled (if available) <br>
Ranking (calculated ratio of "number of matched skills") <br>
Main job detail. <br>
link <br>

Code details: <br>
Scripts prompts user if they want to manually login. If yes: <br>
then script will use login details from a localcred.py file to login <br>
**After running script the first time user should choose no for the log in options (preventing repetitive logins and avoiding detection)**, <br>
doing this will load cookies from previous ranned script and load them to browser. <br>
<br>
Distance" input: allows the user to input a distance in kilometers,if none,the code sets the distance to a default value of 8 km radius<br>
<br>
Script prompts the user to enter a sort by category, and then sorts the end result based on the user's input<br>
<br>
Since not all job adds display the required skills, script will check for that w/ try catch. <br>
<br>
If "skills needed" is present then "ranking" will be calculated, a ratio of "number of matched skills"<br>
<br>
After user input ,a DataFrame is creates as an HTML file with a table representation of the data. The function applies encoding to the DataFrame for email purposes and adds styling features to adjust the column width and prevent overlapping of cell contents. Finally, it saves the HTML file locally.
<br>
Email sending: The function then sets up the SMTP port number and server name for the Gmail SMTP server, and defines the email address to send the email from, as well as the email subject.the send_emails function sends an email with an attached HTML file to each email address in the email_to list using the Gmail SMTP server. The HTML file is generated from the df data and saved locally.<br>

# Script Requirements

- Libraries needed are in requirements.txt
- Download your chromedriver version and place in project this path. 
