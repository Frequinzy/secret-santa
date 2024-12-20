import os
import smtplib
import ssl
import time
import random

from collections import deque

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv

load_dotenv()

s = os.getenv("SENDER_EMAIL")
assert s is not None, "No sender email specified in the .env file"
sender: str = s

p = os.getenv("GOOGLE_APP_PASSWORD")
assert p is not None, "No app password specified in the .env file"
password: str = p

context = ssl.create_default_context()

subject =  "Secret Santa Assignment"
body_template = """\
HoHoHo!

You're the secret santa for {target}.

You have a budget of: {budget}.

The end date is: {end_date}.

Best wishes,
Saint Nicholas
"""

def input_participants(participants):
    print("First enter the emails of all the participants. Type 'done' when done.")
    while True:
        nr = len(participants)
        participant = input(f"Participant nr. {nr}: ")
        if participant == "done":
            break
        participants.append(participant)

def assign_secret_santas(participants):
    random.shuffle(participants)
    targets = deque(participants)
    targets.rotate(1)

    result = dict(zip(participants, targets))
    return result

def main():
    participants = []
    while True:
        input_participants(participants)
        print("The entered particpants are:")
        for i, p in enumerate(participants):
            print(f"Participant nr. {i} is {p}")
        ans = input("Want to redo? y/n ")
        if ans == "n":
            break
        participants = []

    print("Some final questions")
    budget = input("What is the budget for the game? ")
    end_date = input("What is the end date for the game? ")

    santa_assignment = assign_secret_santas(participants)

    if input("Do you want to send emails? y/n ") == "n":
        print(santa_assignment)
        return

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        print(server.login(sender, password))

        for recipent in participants:
            body = body_template.format(
                target=santa_assignment[recipent],
                budget=budget,
                end_date=end_date
            )

            msg = MIMEMultipart()
            msg["From"] = sender
            msg["To"] = recipent
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            time.sleep(2)
            server.sendmail(sender, recipent, msg.as_string())
            print(f"Sent mail to: {recipent}")

if __name__ == "__main__":
    main()
