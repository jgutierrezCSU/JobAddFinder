import pandas as pd
import re
import localcred
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from time import sleep
import unicodedata
import requests
import json

import format_html_results

# for installing packages on cmd : py -m pip install ...


def convert_to_numbs(str1, str2):
    # Remove all non-numeric and non-decimal point characters from str1
    # and convert it to a float
    num1 = float("".join(filter(lambda x: x.isdigit() or x == ".", str1)))

    # Split the time string into a list of words
    words = str2.split()
    # Check if "mins" is less than 10, and convert the "hour" and "mins"
    #  strings to integers
    if len(words) == 4:
        if int(words[2]) < 10:
            hours = int(words[0])
            minutes = int(words[2])
            total_minutes = hours * 100 + int("%02d" % minutes)

        # if mins not less than 10
        else:
            total_minutes = int(words[0]) * 100 + int(words[2])

    # under an hour
    if len(words) == 2:
        total_minutes = int(words[0])

    return (num1, total_minutes)


# Docs https://developers.google.com/maps/documentation/javascript/distancematrix#transit_options
# mode options: BICYCLING ,DRIVING ,TRANSIT (public transit routes.),WALKING
def get_distance(job_main_location, given_origin):

    # Set up the URL for the Google Maps Distance Matrix API request
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric"
    url += "&origins={}".format(given_origin)
    url += "&destinations={}".format(job_main_location)
    url += "&mode=DRIVING"
    url += "&key={}".format(localcred.API_KEY)

    # Make the API request and parse the response
    response = requests.get(url)
    response_json = json.loads(response.text)

    # Check if the response status is OK and extract the distance and duration if so
    if response_json["status"] == "OK":
        distance = response_json["rows"][0]["elements"][0]["distance"]["text"]
        duration = response_json["rows"][0]["elements"][0]["duration"]["text"]
        return distance, duration
    else:
        # Print an error message and return None for distance and duration
        print("Error: {}".format(response_json["status"]))
        return None, None


def calculate_ranking(text):

    """
    Calculate the RANKING rating from the given text.
    Parameters:
    text (str): The text containing the numerator and denominator.
    Returns:
    float: The RANKING rating calculated from the numerator and denominator in the text.
    If the text does not contain both a numerator and a denominator, 0.0 is returned.
    """
    matches = re.findall(r"\d+", text)

    if len(matches) == 2:
        numerator, denominator = map(int, matches)
        # Calculate the RANKING rating
        return numerator / denominator
    else:
        return 0.0


def clean_data(df, sortby_choice, given_origin):
    """
    Cleans and sorts a given pandas dataframe containing job data.

    Args:
        df (pandas.DataFrame): The dataframe to be cleaned and sorted.
        sortby_choice (str): The column name to sort the dataframe by.
            Must be one of the column names in the dataframe.
            If None, the dataframe will not be sorted.
        given_origin (str): The origin location to calculate distance and travel time from.
            Must be a string in the format of "city, state".

    Returns:
        pandas.DataFrame: The cleaned and sorted dataframe.
            The dataframe will have a new "RANKING" column that is calculated based on
            the "MATCHED_SKILLS" column.
            The "DISTANCE_TRAVELTIME" column will also be created based on the
            distance and travel time between the job location and the given origin.
            The dataframe will be sorted by the "sortby_choice" column in ascending
            or descending order, depending on the column type.
            Finally, the dataframe will be saved to a CSV file named "my_data_sorted.csv".

    Raises:
        ValueError: If "sortby_choice" is not a column name in the dataframe.
    """

    columns = [
        "JOB_TITLE",
        "COMPANY_NAME",
        "MAIN_LOCATION",
        "WORK_PLACE_TYPE",
        "DATE_POSTED",
        "SKILLS",
        "MATCHED_SKILLS",
        "MAIN_DETAILS",
        "LINK",
    ]
    df.columns = columns

    # Apply the function to the 'SKILLS' column and create a new 'RANKING' column
    df["RANKING"] = df["MATCHED_SKILLS"].apply(calculate_ranking)
    # Use insert() to move the 'RANKING' column to the second position
    df.insert(1, "RANKING", df.pop("RANKING"))

    # Create a new column called DISTANCE_TRAVELTIME
    df["DISTANCE_TRAVELTIME"] = ""
    df["INT_MIN_DURATION"] = ""
    # Create new Columns
    for index, row in df.iterrows():
        job_main_location = row["MAIN_LOCATION"]
        distance, duration = get_distance(job_main_location, given_origin)

        # Insert the distance and travel time into the new column
        df.at[
            index, "DISTANCE_TRAVELTIME"
        ] = f" {given_origin.split(',')[0]}  ===> {job_main_location.split(',')[0]} is {distance}, Commute is {duration}"

        # Get distance and duration in mins for sorting
        dist_km, dist_mins = convert_to_numbs(distance, duration)
        # Insert duration in mins to last column
        df.at[index, "INT_MIN_DURATION"] = dist_mins

    # Move the 'DISTANCE_TRAVELTIME' column to the 5th position
    df.insert(4, "DISTANCE_TRAVELTIME", df.pop("DISTANCE_TRAVELTIME"))

    if sortby_choice is not None:
        # Sort by given choice
        if sortby_choice == "INT_MIN_DURATION":
            df = df.sort_values([sortby_choice], ascending=[True])
        else:
            df = df.sort_values([sortby_choice], ascending=[False])

    # Concatenate column names and text into a single column, excluding column "main_datails" , can also put a list of columns
    df["SUM_DETAILS"] = df.apply(
        lambda row: "<br><br>".join(
            [f"{col}: {str(row[col])}" for col in df.columns if col != "MAIN_DETAILS"]
        ),
        axis=1,
    )
    # create df with 2 columns
    df = pd.DataFrame(
        {"SUM_DETAILS": df["SUM_DETAILS"], "MAIN_DETAILS": df["MAIN_DETAILS"]}
    )
    # save  df localy w/ 2 columns
    df.to_csv("my_data_sorted.csv", index=False)
    return df


def send_emails(df, email_to):
    """
    Function send_emails:

    Sends an email with an attachment to the specified recipient email address.
    The function takes in a dataframe, df, containing job search results, and the recipient email address, email_to.
    The job search results are formatted and saved locally as an HTML file using the create_html_file function from the format_html_results module.

    Parameters:

    df (pandas DataFrame): A dataframe containing job search results.
    email_to (str): The email address of the recipient.
    Returns:

    None
    """

    # prep/save localy data
    format_html_results.create_html_file(df)

    # Setup port number and server name
    smtp_port = 587  # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server

    email_from = "njdevil707@gmail.com"
    pswd = localcred.email_pword
    # name the email subject
    subject = "Job Results Completed"

    # Make the body of the email
    body = f"""
    Download file then open to use the file properly
    Opening by just clicking file will now allow you 
    use the buttons.
     
    2 Additional raw .csv file were saved locally
    """
    # make a MIME object to define parts of the email
    msg = MIMEMultipart()
    msg["From"] = email_from
    msg["To"] = email_to
    msg["Subject"] = subject

    # Attach the body of the message
    msg.attach(MIMEText(body, "plain"))

    # Define the file to attach,
    # created from create_html_file function
    filename = "results.html"

    # Open the file in python as a binary
    attachment = open(filename, "rb")  # r for read and b for binary

    # Encode as base 64
    attachment_package = MIMEBase("application", "octet-stream")
    attachment_package.set_payload((attachment).read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header(
        "Content-Disposition", "attachment; filename= " + filename
    )
    msg.attach(attachment_package)
    text = msg.as_string()

    # Connect with the server
    print("Connecting to server...")
    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
    TIE_server.starttls()
    TIE_server.login(email_from, pswd)
    print("Succesfully connected to server")
    print()

    # Send emails to "person" as list is iterated
    print(f"Sending email to: {email_to}...")
    TIE_server.sendmail(email_from, email_to, text)
    print(f"Email sent to: {email_to}")

    # Close the port
    TIE_server.quit()


# """ TESTING   """


# def create_html_file2(df):
#     # encode for email
#     df = df.applymap(
#         lambda x: unicodedata.normalize("NFKD", str(x))
#         .encode("ascii", "ignore")
#         .decode("utf-8")
#     )
#     # save locally
#     html_table = df.to_html(
#         render_links=True, justify="justify-all", escape=False, classes="break-word"
#     )

#     # Add CSS styling to adjust column width and prevent overlapping
#     html_table = html_table.replace(
#         "<table", '<table style="table-layout:fixed;width:100%;"'
#     )
#     html_table = html_table.replace("<th></th>", '<th style="width:22px;"></th>')
#     html_table = html_table.replace(
#         "<th>SUM_DETAILS</th>", '<th style="width:30%;">SUM_DETAILS</th>'
#     )
#     html_table = html_table.replace(
#         "<td>", '<td style="max-width:300px;word-wrap:break-word;">'
#     )
#     html_table = html_table.replace("<a ", '<a style="word-wrap:break-word;" ')
#     with open("results.html", "w") as f:
#         f.write(f"<style>table tr td:first-child {{width: 10px;}}</style>\n")
#         f.write(html_table)


# df = pd.read_csv("my_data_raw.csv")
# df = clean_data(df, "INT_MIN_DURATION", "Weinsberg,baden-Württemberg")
# create_html_file2(df)
