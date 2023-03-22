[![Build Status](https://travis-ci.org/jgutierrezCSU/WebScrapperPython.svg?branch=master)](https://travis-ci.org/jgutierrezCSU/WebScrapperPython)

Web scraper for LinkedIn using Python.

Features: <br>
Scrape Jobs using "Job title" , "City" , "State", "Country" and "distance" <br>
Scripts prompts user if they want to manually login (preventing repetitive logins and avoiding detection) <br>
After first log in cookies are saved and no logging in is necessary. <br>  
Script sends an email with the following details after gathering info from site:<br>

<br>

Scraping details include: <br>
Position title <br>
Company name <br>
Main Location <br>
Place of work (could be multiple or remote) <br>
Date posted <br>
Skills needed (if available) <br>
Number of matched skilled (if available) <br>
Ranking (calculated ratio of "number of matched skills")
Main job detail. <br>
link <br>

Code details: <br>
Scripts prompts user if they want to manually login. If yes: <br>
then script will use login details from a localcred.py file to login <br>
After running script the first time user should choose no for the log in options, <br>
doing this will load cookies from previous ranned script and load them to browser. <br>
<br>

Distance" input: allows the user to input a distance in kilometers,the code sets the distance to a default value of 8 km radius
<br>

<br>
Since not all job adds display the required skills, script will check for that w/ try catch. <br>
If "skills needed" is present then "ranking" will be calculated, a ratio of "number of matched skills" <br>
<br>
Email sending: The function then sets up the SMTP port number and server name for the Gmail SMTP server, and defines the email address to send the email from, as well as the email subject.the send_emails function sends an email with an attached HTML file to each email address in the email_to list using the Gmail SMTP server. The HTML file is generated from the df data and saved locally.
