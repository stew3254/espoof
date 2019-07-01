import string
import socket
from exceptions import *

import os

def __is_ip(ip):
    for i in ip: 
        if len([j for j in i if j in string.ascii_letters]) > 0  or "-" in i:
            return False
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def __is_domain(domain):
    subdomains = domain.split(".")
    if len(subdomains) < 2:
        raise InvalidInput("Invalid domain name")
    else:
        is_ip = __is_ip(domain)
        if not is_ip and len([i for i in subdomains if i == ""]) > 0:
            raise InvalidInput("Invalid domain name")
            
def __is_email(email):
    parts = email.split("@")
    if len(parts) != 2:
        raise InvalidInput("Invalid email address '{}'".format(email))
    if len(parts[0]) == 0:
        raise InvalidInput("Invalid email address '{}'".format(email))
    __is_domain(parts[1])

def __validate(prefix, line, line_num, condition):
    if not line.upper().startswith(prefix):
        raise InvalidInput("Line {} must start with '{}' and then the email address".format(line_num, prefix))
    else:
        condition(prefix)

def check(key, value):
    """
    Checks the key and value of an input. If it's bad, raise an exception. If it's good
    add it to the environmental variables so the rest of the scripts can use it
    """
    if key == "domain":
        __is_domain(value)
        try:
            port = int(value.split(":")[1])
            if port < 1 or port > 65535:
                raise InvalidInput("Invalid port number")
        except IndexError:
            return value + ":25"
        except ValueError:
            raise InvalidInput("Invalid port number")
        return value

    elif key == "email":
        if not os.path.isfile(value):
            raise FileNotFound("Email file not found")
        else:
            contents = []
            with open(value, "r") as f:
                contents = f.readlines()
            if len(contents) < 4:
                raise InvalidInput("Please create an email template in the proper format")
            __validate("FROM:", contents[0], 1,
                    condition=lambda prefix: __is_email(contents[0][len(prefix):].split("<")[0].strip())
            )
            __validate("TO:", contents[1], 2,
                    condition=lambda prefix: [__is_email(email.strip()) for email in contents[0][len(prefix):].split(",")]
            )
            __validate("SUBJECT:", contents[2], 3, condition=lambda x: x)
            __validate("BODY:", contents[3], 4, condition=lambda x: x)
    elif key == "file":
        if not os.path.isfile(value):
            raise FileNotFound("File not found")
    elif key == "recipient":
        __is_email(value)
    elif key == "recipient_file":
        if not os.path.isfile(value):
            raise FileNotFound("Recipients file not found")
        else:
            contents = []
            with open(value, "r") as f:
                contents = f.readlines()
            if len(contents) < 1:
                raise InvalidInput("Recipients file must have at least one recipient")
            for email in contents:
                __is_email(email)
    elif key == "sender":
        __is_email(value)
    elif key == "type":
        if not value.lower().startswith("p") and not value.lower().startswith("h"):
            raise InvalidInput("Please choose either plaintext or html")
    elif key == "user":
        __is_email(value)
    elif key == "user_account":
        if not os.path.isfile(value):
            raise FileNotFound("Authentication file not found")
        else:
            contents = []
            with open(value, "r") as f:
                contents = f.readlines()
            if len(contents) < 2:
                raise InvalidInput("Authentication file must have the username on the first line, and the password on the second")
            __is_email(contents[0].strip())
            return contents[0].strip(), contents[1].strip("\n")
