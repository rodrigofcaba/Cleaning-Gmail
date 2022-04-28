
import email
import sys, argparse, re, signal, time, click
from pwn import *
from client import Client

def signal_handler(sig, frame):
    log.info(f"You pressed cntrl+c, exiting...")
    sys.exit(0)

def get_main_parser():
    parser = argparse.ArgumentParser(
        description="This is a basic mail client using Gmail IMAP servers that allows you to delete your unread messages"
    )

    parser.add_argument(
        "email",
        metavar="Email Sender",
        type=str,
        help="Your Gmail address",
    )
    parser.add_argument(
        "password",
        metavar="Password",
        type=str,
        help="The password of the email account used to login to the IMAP server.",
    )

    return parser

def checkEmail(email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    if not re.fullmatch(regex, email):
        return False
    return True

def main():
    parser = get_main_parser()
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)

    if checkEmail(args.email):
        email = args.email
    else:
        log.failure('Please, enter a valid email')
        exit(0)

    password = args.password

    client = Client('imap.gmail.com')

    client.login(email,password)


if __name__ == "__main__":
    main()