from imapclient import IMAPClient
from pwn import *
import click


class Client:

    AVAILABLE_FOLDERS = {
        "Inbox": "INBOX",
        "Drafts": "[Gmail]/Borradores",
        "Important": "[Gmail]/Importantes",
        "Sent": "[Gmail]/Enviados",
        "Spam": "[Gmail]/Spam",
        "Starred": "[Gmail]/Destacados",
        "Trash": "[Gmail]/Papelera",
    }

    AVAILABLE_CRITERIA = {
        "All": "ALL",
        "Unread": "UNSEEN"
    }

    def __init__(self, host):
        self.host = host

    def login(self, username, password):
        log.info("Connecting...")
        self.server = IMAPClient(self.host, ssl=True, port=993)
        self.server.login(username, password)
        log.success("Connected!\n\n")

        print(f"These are the available folders:\n")
        for folder in Client.AVAILABLE_FOLDERS.keys():
            print(folder)

        

    def selectFolder(self):
        while True:
            selectedFolder = input("\nPlease, select one (it is case sensitive):\n")

            if selectedFolder in Client.AVAILABLE_FOLDERS.keys():
                folder = self.server.select_folder(
                    Client.AVAILABLE_FOLDERS[selectedFolder]
                )
                unseenMessages = self.server.search(("UNSEEN"))
                log.info(
                    f"You have a total of %d messages in your {selectedFolder} folder and {len(unseenMessages)} are unread\n"
                    % folder[b"EXISTS"]
                )
                return folder
            else:
                log.failure("Folder not found")

    def searchCriteria(self):

        while True:
            for i in Client.AVAILABLE_CRITERIA:
                print(i)

            criteria = input("\nSelect one of the criteria above (case sensitive)\n")
            if criteria in Client.AVAILABLE_CRITERIA.keys():
                return Client.AVAILABLE_CRITERIA[criteria]
            else:
                log.failure('Invalid criteria\n')

    def deleteMessages(self, messages):
        
        log.warning(f"You are about to delete {len(messages)} messages")

        if click.confirm("Do you want to continue?", default=True):
            self.server.delete_messages(messages)
            self.server.expunge()
            self.server.close_folder()
            log.success(
                "%d messages in your folder have been deleted" % len(messages)
            )
        else:
            log.failure("Operation aborted. No email has been deleted")

        
