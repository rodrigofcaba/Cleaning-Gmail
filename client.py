from imapclient import IMAPClient
from matplotlib.style import available
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

    def __init__(self, host):
        self.host = host

    def login(self, username, password):
        log.info("Connecting...")
        self.server = IMAPClient(self.host, ssl=True, port=993)
        self.server.login(username, password)
        log.success("Connected!\n")

        print(f"These are the available folders:\n")
        for folder in Client.AVAILABLE_FOLDERS.keys():
            print(folder)

        self.folder = self.selectFolder()

        if click.confirm("Do you want to delete them?", default=True):
            self.cleanUnreadMessages()
        else:
            log.failure("Operation aborted. No email has been deleted")

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

    def cleanUnreadMessages(self):
        
        delMsg = self.server.search("UNSEEN")
        log.warning(f"You are about to delete {len(delMsg)} unread messages")

        if click.confirm("Do you want to continue?", default=True):
            self.server.delete_messages(delMsg)
            self.server.expunge()
            self.server.close_folder()
            log.success(
                "%d unread messages in your folder have been deleted" % len(delMsg)
            )
        else:
            log.failure("Operation aborted. No email has been deleted")

        self.server.logout()
