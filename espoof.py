#!/usr/bin/python3

from email.headerregistry import Address
from email.message import EmailMessage
from getpass import getpass
from exceptions import *
import smtplib
import sys
import argParse
import checkArgs

def create_email_message(from_address, to_address, subject, plain, html=None):
    msg = EmailMessage()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.set_content(plain)
    if args.file is not None:
        print(args.file)
        with open(args.file, "r") as f:
            msg.add_attachment(f.read(), filename=args.file)
    if html is not None:
        msg.add_alternative(html, subtype="html")
    return msg

args = argParse.parse()
domain = args.domain.split(":")[0]
port = int(args.domain.split(":")[1])
recipients = []
subject = None
body = None

if args.email is None:
    if args.sender is None:
        while True:
            sender = input("FROM: ")
            try:
                checkArgs.check("sender", sender)
                parts = sender.split("<")
                args.sender = parts[0].strip()
                if len(parts) > 1:
                    args.name = parts[1].replace(">", "").strip()
                break
            except InvalidInput as e:
                print("Please enter a valid email address")
    if args.recipient is None and args.recipient_file is None:
        while True:
            recipient = input("TO: ")
            try:
                checkArgs.check("recipient", recipient)
                recipients.append(recipient)
                break
            except InvalidInput as e:
                print("Please enter a valid email address")
    elif args.recipient_file is not None:
        with open(args.recipient_file, "r") as f:
            recipients = f.readlines()
    if args.recipient is not None:
        recipients.append(args.recipient)

    subject = input("SUBJECT: ")
    body = []
    print("When you are done writing to the body, just write END on the last line by itself")
    while True:
        part = input("BODY: ")
        if part == "END":
            break
        else:
            body.append(part+"\n")
    body = "".join(body)[:-1]
else:
    with open(args.email, "r") as f:
        contents = f.readlines()
    # Get from
    parts = contents[0][len("FROM:"):].split("<")
    args.sender = parts[0].strip()
    if len(parts) > 1:
        args.name = parts[1].replace(">", "").strip()
    # Get recipient(s)
    recipients = contents[1][len("TO:"):].strip().split(",")
    # Get subject
    subject = contents[2][len("SUBJECT:"):].strip()
    # Get body
    body_parts = []
    if len(contents) > 4:
        for part in contents[4:]:
            body_parts.append(part.rstrip())
    body = "\n".join(body_parts)

if args.user is None:
    while True:
        user = input("USERNAME: ")
        try:
            checkArgs.check("user", user)
            args.user = user
            break
        except InvalidInput as e:
            print("Please enter a valid email address")

if args.password is None:
    args.password = getpass("PASSWORD: ")

if args.name is None:
    args.name = ""
sender = (
    Address(display_name=args.name, username=args.sender.split("@")[0], domain=args.sender.split("@")[1]),
)

for person in recipients:
    person = person.strip()
    # Recipent
    recipient = (
        Address(username=person.split("@")[0], domain=person.split("@")[1]),
    )

    msg = create_email_message(from_address=sender, to_address=recipient, subject=subject, plain=body)

    with smtplib.SMTP(domain, port=port) as smtp_server:
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(args.user, args.password)
        smtp_server.send_message(msg)

    print("Email sent successfully to {}".format(person.strip()))
