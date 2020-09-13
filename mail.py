import pprint
from uuid import uuid4

from imap_tools import MailBox
from rich import inspect, print

HOST = "imap.fastmail.com"
USERNAME = "klops@fastmail.com"
PASSWORD = "rybvb7c275ywquu3"


class MailMessage:
    def __init__(self, sender, subject, year, month, day, content, filename=None):
        self.sender = sender
        self.subject = subject
        self.year = year
        self.month = month
        self.day = day
        self.content = content
        self.filename = filename
        self.uuid = uuid4()

    def __hash__(self):
        return hash(self.uuid)


class FilenameGenerator:
    def __init__(self):
        self.known_subjects = dict()

    def get_filename(self, mail: MailMessage):
        desired_name = f"{mail.sender}-{mail.subject}"
        if desired_name not in self.known_subjects:
            self.known_subjects[desired_name] = 0
        else:
            self.known_subjects[desired_name] += 1
            desired_name = f"{desired_name}-{self.known_subjects[desired_name]}"
        return desired_name


filename_generator = FilenameGenerator()
mails = set()
folders = set()

def create_topics(mbox):
    folders_mailbox = mbox.folder.list()
    return [folder["name"] for folder in folders_mailbox]


def create_mail_obj(message):
    mail = MailMessage(
        sender=message.from_,
        subject=message.subject[:10],
        year=str(message.date.year),
        month=str(message.date.month),
        day=str(message.date.day),
        content=bytes(msg.html, encoding="utf-8"),
    )
    mail.filename = filename_generator.get_filename(mail)
    return mail


with MailBox(HOST).login(USERNAME, PASSWORD) as mailbox:
    folders_dict = dict.fromkeys(create_topics(mailbox))
    for folder_name in folders_dict.keys():
        folders_dict[folder_name] = set()
        mailbox.folder.set(folder_name) # lists folders in specific mailbox
        for msg in mailbox.fetch():
            mail = create_mail_obj(msg)
            mails.add(mail)  # creates set of all messages in mailbox

            folders_dict[folder_name].add(mail)


topics_dict = {f"/{key}": value for key, value in folders_dict.items()}
print(f"{topics_dict=}")


mails_dict = {}
for mail in mails:
    if mail.year not in mails_dict:
        mails_dict[mail.year] = {}
    if mail.month not in mails_dict[mail.year]:
        mails_dict[mail.year][mail.month] = {}
    if mail.day not in mails_dict[mail.year][mail.month]:
        mails_dict[mail.year][mail.month][mail.day] = {}
    if mail not in mails_dict[mail.year][mail.month][mail.day]:
        mails_dict[mail.year][mail.month][mail.day][mail.filename] = mail.content

senders_dict = {}
for mail in mails:
    if mail.sender not in senders_dict:
        senders_dict[mail.sender] = {}
    if mail not in senders_dict[mail.sender]:
        senders_dict[mail.sender][mail.filename] = mail.content

if __name__ == "__main__":
    pprint.pprint("00_00")
