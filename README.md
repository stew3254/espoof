# espoof
The Email Spoofing Tool

```
# ./espoof.py smtp.mailserver.com
```

Example help command:

```
$ ./espoof.py -h
Usage: ./espoof.py [OPTIONS] <domain>
espoof.py - the email spoofing tool

OPTIONS:
  -e--email           <email>            Email format file to read in from
  -f--file            <file>             File(s) to upload with the email. Delimeted by a comma
  -h--help            <help>             Used to display this page
  -p--password        <password>         Password of the SMTP login
  -n--name            <name>             Name of a recipient. This must be used with the -r flag
  -r--recipient       <recipient>        Recipient(s) of the email. Delimited by a comma
  -R--recipient_file  <recipient_file>   Recipient file to read from
  -s--sender          <sender>           Sender of the email
  -t--type            <type>             Set the content type (plain or html)
  -u--user            <user>             Username of the SMTP login
  -U--user_account    <user_account>     File for account information
  -v--verbose         <verbose>          increase output verbosity

Examples:
  ./espoof.py mail.server.com
  ./espoof.py -u user@domain.com -t p smpt.server.com:587
  ./espoof.py -U account.txt -f my.pdf -t html -e email.txt 127.0.0.1:1337
```
