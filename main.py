#!/usr/bin/env python
import os.path
if not os.path.exists("config.toml"):
    print("*****")
    print("You need to have a config.toml for this application to work, check config.toml.example for options")
    print("*****")
    exit(1)

from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from ollama import chat
from tqdm import tqdm
import csv
import logging
import markdown
import os
import smtplib, ssl
import tomllib

LOGGING_LEVEL=os.environ.get("DEBUG", "INFO")

start_time = datetime.now()
if LOGGING_LEVEL:
    logging.basicConfig(filename="log/main_logging.log",
                        level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",)
else:
    logging.basicConfig(filename="log/main_logging.log",
                        level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",)

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

port = config["SMTP_PORT"]
password = input("SMTP password: ")
sender_email = config["SMTP_SENDER_EMAIL"]

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("email.html.j2")

with open(config["CSV_FILE"]) as data_file:
    data = csv.DictReader(data_file)
    data_list = []
    for row in data:
        data_list.append(row)

event_website = config["EMAIL_EVENT_WEBSITE"]
template_email = config["EMAIL_TEMPLATE"]
logo_url = config["EMAIL_LOGO_URL"]

your_name = config["YOUR_NAME"]
your_email = config["YOUR_EMAIL"]

context = ssl.create_default_context()
with smtplib.SMTP_SSL(config["SMTP_SERVER"], port, context=context) as server:
    server.login(sender_email, password)

    for i in tqdm(data_list, desc="Sending emails to..."):

        receiver_email = i['email']

        response = chat(model=config["OLLAMA_AI_MODEL"], messages= [
        {
            'role': 'user',
            'content': f"""
            You are a professional cold caller for sponsorships for 50c3. You
            write friendly engaging emails to help drive people to want to
            sponsor your events. You use the following information and template
            email to help write out unique and engaging conversational emails:
            {template_email}. The event website is located at this url:
            {event_website}. Write an email that convinces me and the recipient
            of this email to want to sponsor this organization. The recipients
            name is {i['name']}. The email is from my name which is
            {your_name}, and my email address and {your_email}. Please do not
            put the Subject at the top of the email, or mention any company I
            work for. Do not add my phone number or my title.
            """,
        },]
    )

        message = MIMEMultipart("alternative")
        message["Subject"] = config["EMAIL_SUBJECT"]
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Reply-To"] = f"fof@nwsoftball.org"

        raw_response =  response['message']['content']
        text_email = raw_response

        markdown_email = markdown.markdown(raw_response)
        html_email = template.render(content=markdown_email,
                                     logo_url=logo_url
                                    )
        part1 = MIMEText(text_email, "plain")
        part2 = MIMEText(html_email, "html")

        message.attach(part1)
        message.attach(part2)
        logging.debug(f"")
        logging.debug(f"Sending email to {receiver_email}...")
        logging.debug(f"")
        logging.debug(f"Email: {message.as_string()}")

        server.sendmail(sender_email, receiver_email, message.as_string())
        logging.info(f">>>> email sent to {i['email']} <<<<<")
        print(f">>>> email sent to {i['email']} <<<<<")

print(f"This took {datetime.now() - start_time} to run")
logging.info(f"This took {datetime.now() - start_time} to run")
