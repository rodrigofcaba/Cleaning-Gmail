import sys, argparse, re, signal, click, os
from pwn import *
from client import Client
from dotenv import load_dotenv


def signal_handler(sig, frame):
    print("")
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
        "-p",
        "--password",
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


def checkPassword(args):

    if args.password:
        return args.password
    elif os.environ.get("PASSWORD"):
        print("here")
        return os.environ.get("PASSWORD")
    else:
        pwd = input("\nNo password stored, please enter your password:\n")
        return pwd


def main():
    load_dotenv()
    parser = get_main_parser()
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)

    if checkEmail(args.email):
        email = args.email
    else:
        log.failure("Please, enter a valid email")
        exit(0)

    password = checkPassword(args)

    client = Client("imap.gmail.com")

    client.login(email, password)
    os.environ["PASSWORD"] = password

    client.folder = client.selectFolder()

    if click.confirm("Do you want to delete some of those?", default=True):
        criteria = client.searchCriteria()
        delMsg = client.server.search(criteria)
        client.deleteMessages(delMsg)

    else:
        log.failure("Operation aborted. No email has been deleted")

    log.info("Logging out...")
    client.server.logout()
    log.success("Connection closed.")


if __name__ == "__main__":
    main()
