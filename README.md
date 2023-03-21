[![Build Status](https://travis-ci.org/jgutierrezCSU/WebScrapperPython.svg?branch=master)](https://travis-ci.org/jgutierrezCSU/WebScrapperPython)

Web scraper for LinkedIn using Python.

Features: <br>
Scrape Jobs using "Job title" , "City" , "State" and "Country" <br>
Scripts prompts user if they want to manually login (preventing repetitive logins and avoiding detection) <br>
After first log in cookies are saved and no logging in is necessary. <br>  
<br>

Scraping details include: <br>
Position title <br>
Company name <br>
Main Location <br>
Place of work (could be multiple or remote) <br>
Date posted <br>
Skills needed (if available) <br>
Main job detail. <br>

Code details: <br>
Scripts prompts user if they want to manually login. If yes: <br>
then script will use login details from a localcred.py file to login <br>
<br>
Since not all job adds display the required skills, script will check for that w/ try catch. <br>
