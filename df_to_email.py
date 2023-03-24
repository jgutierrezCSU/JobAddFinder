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
        # Calculate the RANKING rating
        return numerator / denominator
    else:
        return 0.0


def clean_data(df):

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

    # "RANKING" column is now sorted in descending order while keeping the "MAIN_LOCATION" column sorted in ascending order.
    df = df.sort_values(["MAIN_LOCATION", "RANKING"], ascending=[True, False])

    #save raw df locally before creating just 3 columns
    df.to_csv('my_data_raw.csv', index=False)

    # Concatenate column names and text into a single column, excluding column "main_datails" , can also put a list of columns
    df['concatenated_text'] = df.apply(lambda row: '<br><br>'.join([f"{col}: {str(row[col])}" for col in df.columns if col != 'MAIN_DETAILS']), axis=1)
    #create df with 2 columns
    df = pd.DataFrame({"concatenated_text": df["concatenated_text"], "MAIN_DETAILS": df["MAIN_DETAILS"]})

    #save  df localy w/ 2 columns
    df.to_csv('my_data_sorted.csv', index=False)
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
    html_table = html_table.replace('<th></th>', '<th style="width:10px;"></th>')
    html_table = html_table.replace('<th>concatenated_text</th>', '<th style="width:30%;">concatenated_text</th>')
    html_table = html_table.replace('<td>', '<td style="max-width:300px;word-wrap:break-word;">')
    html_table = html_table.replace('<a ', '<a style="word-wrap:break-word;" ')
    with open("results2.html", "w") as f:
        f.write(f'<style>table tr td:first-child {{width: 10px;}}</style>\n')
        f.write(html_table)


def send_emails(df, email_to):
    # prep/save localy data
    create_html_file(df)
    


    # Setup port number and server name
    smtp_port = 587  # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server

    email_from = "njdevil707@gmail.com"
    pswd = localcred.email_pword
    # name the email subject
    subject = "Job Results Completed"

    for person in email_to:

        # Make the body of the email
        body = f"""
        Results file in html (click and should open in seperate window). 
        2 Additional raw .csv file were saved localy
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

""" TESTING   """


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

"""                            """
# def highlight_keyword(s, keyword):
#     s = str(s)
#     if keyword in s:
#         start_idx = s.find(keyword)
#         end_idx = start_idx + len(keyword)
#         highlighted = f'<span style="background-color: yellow">{keyword}</span>'
#         return s[:start_idx] + highlighted + s[end_idx:]
#     else:
#         return s
    
# def highlight_keyword_italic_lightgreen(s, keyword):
#     s = str(s)
#     if keyword in s:
#         start_idx = s.find(keyword)
#         end_idx = start_idx + len(keyword)
#         highlighted = f'<span style="background-color: #c8e6c9">{keyword}</span>'
#         return s[:start_idx] + highlighted + s[end_idx:]
#     else:
#         return s



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
#     html_table = html_table.replace('<th></th>', '<th style="width:10px;"></th>')
#     html_table = html_table.replace('<th>concatenated_text</th>', '<th style="width:30%;">concatenated_text</th>')
#     html_table = html_table.replace('<td>', '<td style="max-width:300px;word-wrap:break-word;">')
#     html_table = html_table.replace('<a ', '<a style="word-wrap:break-word;" ')
#     with open("results2.html", "w") as f:
#         f.write(f'<style>table tr td:first-child {{width: 10px;}}</style>\n')
#         f.write(html_table)



# # read CSV file and create HTML file
# df=pd.read_csv('my_data_w-colm.csv')
# create_html_file2(df)


# # Save the HTML to a file
# with open("results2.html", "w") as f:
#     f.write(df)