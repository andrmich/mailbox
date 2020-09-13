from collections import defaultdict

from imap_tools import MailBox, AND
import pprint
from rich import print

HOST = "imap.fastmail.com"
USERNAME = "klops@fastmail.com"
PASSWORD = "rybvb7c275ywquu3"


# get list of email subjects from INBOX folder


class MailMessage:
    def __init__(self, sender, subject, uid, year, month, day, filename=None):
        self.sender = sender
        self.subject = subject
        self.uid = uid
        self.year = year
        self.month = month
        self.day = day
        self.filename = filename


class AllMessages(dict):
    def __init__(self):
        self.known_subjects = dict()
        super().__init__()

    def rename_and_insert(self, mail: MailMessage):
        desired_name = f"{mail.sender}-{mail.subject}"
        if desired_name not in self:
            self[desired_name] = mail.sender
            self.known_subjects[desired_name] = 0
            return
        self.known_subjects[desired_name] += 1
        self[f"{desired_name}-{self.known_subjects[desired_name]}"] = mail.sender

    def return_filename(self, content=None):
        for key, value in self.items():
            if value == content:
                return key


class DateDict:
    def __init__(self, year, month, day, filename, uid):
        self.year = year
        self.month = month
        self.day = day
        self.filename = filename
        self.uid = uid

    def __dict__(self):
        return {self.year: {self.month: self.day}}

    def __iter__(self):
        yield from {self.year: {self.month: self.day}}.items()


all_messages = AllMessages()
content_dct = defaultdict(bytes)
fil_name_dct = {}
mails = set()
dates = set()
folder_uid_dct = {}
folders = set()

with MailBox(HOST).login(USERNAME, PASSWORD) as mailbox:

    # messages = mailbox.fetch(AND(all=True))
    folders_mailbox = mailbox.folder.list()  # lists folders in specific mailbox
    folder_names = [folder["name"] for folder in folders_mailbox]
    messages_dict_sender = defaultdict(set)
    messages_dict_folders = defaultdict(set)
    for folder_name in folder_names:
        mailbox.folder.set(folder_name)
        folders.add(folder_name)
        folder_uid_dct[folder_name] = set()
        for msg in mailbox.fetch():
            uid = hash(msg)
            mail = MailMessage(sender=msg.from_, subject=msg.subject[:10], uid=uid, year=str(msg.date.year),
                        month=str(msg.date.month), day=str(msg.date.day))
            mails.add(mail)
            all_messages.rename_and_insert(mail)
            fil_name = all_messages.return_filename(mail.sender)
            mail.filename = fil_name
            dates.add(
                (
                    DateDict(
                        year=str(msg.date.year),
                        month=str(msg.date.month),
                        day=str(msg.date.day),
                        filename=fil_name,
                        uid=uid,
                    )
                )
            )
            content_dct[uid] = msg.text
            fil_name_dct[uid] = fil_name

            folder_uid_dct[folder_name].add(uid)

# print(folder_uid_dct)
# print(folders)
new_folder_uid_dict = {f"/{key}": value for key, value in folder_uid_dct.items()}
print(f"{new_folder_uid_dict=}")

# dates_dict = {}
# for date in dates:
#     if date.year not in dates_dict:
#         dates_dict[date.year] = {}
#     if date.month not in dates_dict[date.year]:
#         dates_dict[date.year][date.month] = {}
#     if date.day not in dates_dict[date.year][date.month]:
#         dates_dict[date.year][date.month][date.day] = {}
#     if date.uid not in dates_dict[date.year][date.month][date.day]:
#         dates_dict[date.year][date.month][date.day][fil_name_dct[date.uid]] = date.uid
#         # dates_dict[date.year][date.month][date.day][fil_name_dct[date.uid]] = content_dct[date.uid]
mails_dict = {}
for mail in mails:
    if mail.year not in mails_dict:
        mails_dict[mail.year] = {}
    if mail.month not in mails_dict[mail.year]:
        mails_dict[mail.year][mail.month] = {}
    if mail.day not in mails_dict[mail.year][mail.month]:
        mails_dict[mail.year][mail.month][mail.day] = {}
    if mail.uid not in mails_dict[mail.year][mail.month][mail.day]:
        mails_dict[mail.year][mail.month][mail.day][fil_name_dct[mail.uid]] = content_dct[mail.uid]
        # dates_

senders_dict = {}
for mail in mails:
    if mail.sender not in senders_dict:
        senders_dict[mail.sender] = {}
    if mail.uid not in senders_dict[mail.sender]:
        senders_dict[mail.sender][fil_name_dct[mail.uid]] = content_dct[mail.uid]
        # senders_dict[mail.sender][fil_name_dct[mail.uid]] = content_dct[mail.uid]
# #
# pprint.pprint(mails_dict)
# pprint.pprint(senders_dict)

# def nested_dict():
#     """
#     Creates a default dictionary where each value is an other default dictionary.
#     """
#     return defaultdict(nested_dict)
#
#
# def default_to_regular(d):
#     """
#     Converts defaultdicts of defaultdicts to dict of dicts.
#     """
#     if isinstance(d, defaultdict):
#         d = {k: default_to_regular(v) for k, v in d.items()}
#     return d
#
#
# def get_path_dict(paths):
#     new_path_dict = nested_dict()
#     for path in paths:
#         parts = path.split('/')
#         if parts:
#             # marcher = new_path_dict
#             for key in parts[:-1]:
#                 marcher = new_path_dict[key]
#                 print(f"{parts[-1]}")
#                 print(f"{path=}")
#                 marcher[(parts[-1])] = 'lol'
#                 # marcher[(parts[-1])] =  set()
#
#     return default_to_regular(new_path_dict)
#
# folders_dict = get_path_dict(folders)

# pprint.pprint(folders_dict)


if __name__ == "__main__":
    # print(set(mhs))
    # pprint.pprint(all_messagesgs.values().__dict__['month'])
    pprint.pprint("00_00")
