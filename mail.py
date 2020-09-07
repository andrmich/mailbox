from imap_tools import MailBox, AND
import pprint

HOST = "imap.fastmail.com"
USERNAME = "klops@fastmail.com"
PASSWORD = "rybvb7c275ywquu3"


# get list of email subjects from INBOX folder


class MailMessage:
    def __init__(self, year, month, day, sender, subject, IMAP_folder):
        self.year = year
        self.month = month
        self.day = day
        self.sender = sender
        self.subject = subject
        self.folder = IMAP_folder

    def create_email_object(self):
        pass


class AllMessages(dict):
    def __init__(self):
        self.known_subjects = dict()
        super().__init__()

    def rename_and_insert(self, elem: MailMessage):
        desired_name = f"{elem.sender}-{elem.subject}"
        if desired_name not in self:
            self[desired_name] = elem
            self.known_subjects[desired_name] = 0
            return
        self.known_subjects[desired_name] += 1
        self[f"{desired_name}-{self.known_subjects[desired_name]}"] = elem


all_messages = AllMessages()

with MailBox(HOST).login(USERNAME, PASSWORD) as mailbox:
    # messages = mailbox.fetch(AND(all=True))
    folders = mailbox.folder.list()  # lists folders in specific mailbox
    folder_names = [folder["name"] for folder in folders]

    for folder_name in folder_names:
        mailbox.folder.set(folder_name)
        for msg in mailbox.fetch():
            year = msg.date.year
            month = msg.date.month
            day = msg.date.day
            sender = msg.from_
            subject = msg.subject
            element = MailMessage(
                year=year,
                month=month,
                day=day,
                sender=sender,
                subject=subject,
                IMAP_folder=folder_name,
            )
            print(element)
            all_messages.rename_and_insert(element)


if __name__ == "__main__":
    pprint.pprint(sorted(all_messages.keys()))
