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

import unicodedata


def calculate_ranking(text):
    matches = re.findall(r"\d+", text)

    if len(matches) == 2:
        numerator, denominator = map(int, matches)
        # Calculate the ranking rating
        return numerator / denominator
    else:
        return 0.0


def clean_data(df):

    columns = [
        "job_title",
        "company_name",
        "main_location",
        "work_place_type",
        "date_posted",
        "skills",
        "matched_skills",
        "main_details",
        "link",
    ]
    df.columns = columns

    # Apply the function to the 'Skills' column and create a new 'Ranking' column
    df["ranking"] = df["matched_skills"].apply(calculate_ranking)

    # "ranking" column is now sorted in descending order while keeping the "main_location" column sorted in ascending order.
    df = df.sort_values(["main_location", "ranking"], ascending=[True, False])
    # Print the result
    # print(df[["job_title", "company_name", "main_location", "ranking", "link"]])
    # df.to_csv("trash.csv", index=False)
    return df


""" send to email"""


def create_html_file(df):
    # encode for email
    df = df.applymap(
        lambda x: unicodedata.normalize("NFKD", str(x))
        .encode("ascii", "ignore")
        .decode("utf-8")
    )
    # save localy
    html_table = df.to_html()
    with open("results.html", "w") as f:
        f.write(html_table)


# Define the email function (dont call it email!)


def send_emails(df, email_to):
    # prep/save localy data
    create_html_file(df)

    # Setup port number and server name
    smtp_port = 587  # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server

    email_from = "njdevil707@gmail.com"
    pswd = localcred.email_pword
    # name the email subject
    subject = "New email from with attachments!!"

    for person in email_to:

        # Make the body of the email
        body = f"""
        Results in .html
        """

        # make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg["From"] = email_from
        msg["To"] = person
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

        # # Cast as string
        text = msg.as_string()

        # Connect with the server
        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        print("Succesfully connected to server")
        print()

        # Send emails to "person" as list is iterated
        print(f"Sending email to: {person}...")
        TIE_server.sendmail(email_from, person, text)
        # TIE_server.sendmail(email_from, person, text)
        print(f"Email sent to: {person}")
        print()

    # Close the port
    TIE_server.quit()
