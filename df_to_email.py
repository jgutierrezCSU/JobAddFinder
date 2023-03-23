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
    # Use insert() to move the 'Ranking' column to the second position
    df.insert(1, "ranking", df.pop("ranking"))

    # "ranking" column is now sorted in descending order while keeping the "main_location" column sorted in ascending order.
    df = df.sort_values(["main_location", "ranking"], ascending=[True, False])

    # Concatenate column names and text into a single column, excluding column "main_datails" , can also put a list of columns
    df['concatenated_text'] = df.apply(lambda row: '<br><br>'.join([f"{col}: {str(row[col])}" for col in df.columns if col != 'main_details']), axis=1)
    #create df with 2 columns
    df = pd.DataFrame({"concatenated_text": df["concatenated_text"], "main_details": df["main_details"]})

    return df


""" send to email"""


def create_html_file(df):
    # encode for email
    df = df.applymap(
        lambda x: unicodedata.normalize("NFKD", str(x))
        .encode("ascii", "ignore")
        .decode("utf-8")
    )
    # save locally
    html_table = df.to_html(
        render_links=True, 
        justify="justify-all", 
        escape=False, 
        classes="break-word"
    )
    
    # Add CSS styling to adjust column width and prevent overlapping
    html_table = html_table.replace('<table', '<table style="table-layout:fixed;width:100%;"')
    html_table = html_table.replace('<th>concatenated_text</th>', '<th style="width:30%;">concatenated_text</th>')
    html_table = html_table.replace('<th>main_details</th>', '<th style="width:70%;">main_details</th>')
    html_table = html_table.replace('<td>', '<td style="max-width:300px;word-wrap:break-word;">')
    html_table = html_table.replace('<a ', '<a style="word-wrap:break-word;" ')
    with open("results.html", "w") as f:
        f.write(html_table)


def send_emails(df, email_to):
    # prep/save localy data
    create_html_file(df)
    #save localy
    df.to_csv('my_data.csv', index=False)


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


# for page_num in range(1, 15):
#     print(25 * (page_num - 1))

# num_of_jobs = int(input("Enter max number of jobs to get (1-100): "))

# if num_of_jobs < 1 or num_of_jobs > 100:
#     print("Invalid input! Please enter a number between 1 and 100.")
# else:
#     page = (num_of_jobs - 1) // 25 + 1
#     #print(page)
# for x in range(1, page+1):
#     print(x)



# def create_html_file2(df):
#     # encode for email
#     df = df.applymap(
#         lambda x: unicodedata.normalize("NFKD", str(x))
#         .encode("ascii", "ignore")
#         .decode("utf-8")
#     )
#     # save locally
#     html_table = df.to_html(
#         render_links=True, 
#         justify="justify-all", 
#         escape=False, 
#         classes="break-word"
#     )
    
#     # Add CSS styling to adjust column width and prevent overlapping
#     html_table = html_table.replace('<table', '<table style="table-layout:fixed;width:100%;"')
#     html_table = html_table.replace('<th>concatenated_text</th>', '<th style="width:30%;">concatenated_text</th>')
#     html_table = html_table.replace('<th>main_details</th>', '<th style="width:70%;">main_details</th>')
#     html_table = html_table.replace('<td>', '<td style="max-width:300px;word-wrap:break-word;">')
#     html_table = html_table.replace('<a ', '<a style="word-wrap:break-word;" ')

#     with open("results2.html", "w") as f:
#         f.write(html_table)


# df=pd.read_csv('my_data.csv')

# # Concatenate column names and text into a single column, excluding column "main_datails" , can also put a list of columns
# df['concatenated_text'] = df.apply(lambda row: '<br><br>'.join([f"{col}: {str(row[col])}" for col in df.columns if col != 'main_details']), axis=1)


# # Print the updated DataFrame
# # print(df["concatenated_text"],["main_details"])
# df2 = pd.DataFrame({"concatenated_text": df["concatenated_text"], "main_details": df["main_details"]})
# df2.to_csv('my_data2.csv', index=False)
# print(df2)
# create_html_file2(df2)