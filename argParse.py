import argparse
import checkArgs
import sys

#Hacks to make argparse look pretty
class HelpFormatter(argparse.RawTextHelpFormatter):

    #Print in a pretty format
    def _format_action_invocation(self, action):
        ret = ''
        for item in list(action.option_strings) + ['<{}>'.format(action.dest)]:
            if len(item) < 4:
                ret += f'{item:4}'
            else:
                ret += f'{item:18}'
        return ret

    #Formats the text in help
    def _format_action(self, action):
        width = 24
        return f"  {self._format_action_invocation(action):{width}} {action.help}\n"

    #Reset usage name and strip extra newline character
    def _format_usage(self, usage, actions, groups, prefix):
        return super()._format_usage(usage, actions, groups, "Usage: ")[:-1]

def parse():
    #Help the program displays
    program = sys.argv[0]
    description = "{} - the email spoofing tool".format(program.split("/")[-1])
    usage = "{} [OPTIONS] <domain>".format(program)
    epilog = """Examples:
  {} mail.server.com
  {} -u user@domain.com -t p smpt.server.com:587
  {} -U account.txt -f my.pdf -t html -e email.txt 127.0.0.1:1337""".format(program, program, program)

    #Create the parser
    parser = argparse.ArgumentParser(add_help=False, description=description, usage=usage, prog=program,
                                                                     epilog=epilog, formatter_class=HelpFormatter)

    #Add a new group to the parser and then add the subsequent arguments to it
    group = parser.add_argument_group("OPTIONS")
    group.add_argument("domain", help=argparse.SUPPRESS)

    #Add optional arguemnts
    group.add_argument("-e", "--email", help="Email format file to read in from", type=str)
    group.add_argument("-f", "--file", help="File(s) to upload with the email. Delimeted by a comma", type=str)
    group.add_argument("-h", "--help", help="Used to display this page", action="help")
    group.add_argument("-p", "--password", help="Password of the SMTP login", type=str)
    group.add_argument("-n", "--name", help="Name of a recipient. This must be used with the -r flag", type=str)
    group.add_argument("-r", "--recipient", help="Recipient(s) of the email. Delimited by a comma", type=str)
    group.add_argument("-R", "--recipient_file", help="Recipient file to read from", type=str)
    group.add_argument("-s", "--sender", help="Sender of the email", type=str)
    group.add_argument("-t", "--type", help="Set the content type (plain or html)", type=str)
    group.add_argument("-u", "--user", help="Username of the SMTP login", type=str)
    group.add_argument("-U", "--user_account", help="File for account information", type=str)
    group.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

    #If no parameters are invoked, run the help command
    args = parser.parse_args()

    #Check arguments
    if args.email is not None:
        checkArgs.check("email", args.email)
    if args.file is not None:
        checkArgs.check("file", args.file)
    if args.recipient is not None:
        checkArgs.check("recipient", args.recipient)
        if args.name is not None:
            checkArgs.check("name", args.name)
    if args.recipient_file is not None:
        checkArgs.check("recipient_file", args.recipient_file)
    if args.sender is not None:
        checkArgs.check("sender", args.sender)
    if args.type is not None:
        checkArgs.check("type", args.type)

    #Check only if the others don't exist
    if (args.user_account is not None and args.user is not None) or (args.user_account is not None and args.password is not None):
        print("Error: Cannot use -U flag with either -u or -p. Please choose -U only or the others")
        exit(1)
    elif args.user_account is not None:
        args.user, args.password = checkArgs.check("user_account", args.user_account)
    elif args.user is not None:
        checkArgs.check("user", args.user)
    if args.password is not None:
        checkArgs.check("password", args.password)

    args.domain = checkArgs.check("domain", args.domain)

    return args 

