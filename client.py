import click
from imapclient import IMAPClient
from pwn import *

from color import Color


class Client:

    AVAILABLE_CRITERIA = {"All": "ALL", "Unread": "UNSEEN"}
    formatter = Color()

    def __init__(self, host):
        self.host = host
        self.server = IMAPClient(self.host, ssl=True, port=993)

    def login(self, username, password):
        log.info("Connecting...")

        try:
            self.server.login(username, password)
            log.success("Connected!\n")

            self.getAvailableFolders()

        except:
            log.failure(
                "Incorrect password. Make sure you use your own application-specific password."
            )
            exit(0)

    def getAvailableFolders(self):
        self.FOLDERS = [
            folder for tags, directory, folder in self.server.list_folders()
        ]

    def selectFolder(self):

        selectedFolder = ""

        message = "\nPlease, select a folder (use the number on the left):\n\n"

        for index, item in enumerate(self.FOLDERS):
            message += f"{index+1}) {item}\n"

        while True:
            selectedFolder = input(message)

            if selectedFolder in map(str, range(1, len(self.FOLDERS) + 1)):
                folder = self.server.select_folder(
                    self.FOLDERS[int(selectedFolder) - 1]
                )
                unseenMessages = self.server.search(("UNSEEN"))

                formattedFolder = self.formatter.bold(
                    self.FOLDERS[int(selectedFolder) - 1]
                )
                formattedNrOfMessages = self.formatter.bold(folder[b"EXISTS"])
                log.info(
                    f"You have a total of {formattedNrOfMessages} messages in your {formattedFolder} folder and {self.formatter.bold(len(unseenMessages))} are unread\n"
                )
                return folder
            else:
                log.failure(f"Folder {selectedFolder} not found.\n")

    def searchCriteria(self):
        message = "\nWhich ones you want to delete (case sensitive)?\n"

        for i in Client.AVAILABLE_CRITERIA:
            message += f"{i}\n"
        while True:
            criteria = input(message)

            if criteria in Client.AVAILABLE_CRITERIA.keys():
                return Client.AVAILABLE_CRITERIA[criteria]
            else:
                log.failure("Invalid criteria\n")

    def deleteMessages(self, messages):

        log.warning(
            f"{self.formatter.RED} You are about to delete {len(messages)} messages {self.formatter.END}"
        )

        if click.confirm("Do you want to continue?", default=True):
            self.server.delete_messages(messages)
            self.server.expunge()
            self.server.close_folder()
            log.success(
                f"{self.formatter.bold(len(messages))} messages in your folder have been deleted"
            )
        else:
            log.failure(f"Operation aborted. No email has been deleted")
