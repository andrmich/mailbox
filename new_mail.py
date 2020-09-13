from typing import Set, Any

from imap_tools import MailBox
from imbox import Imbox
import email
from collections import defaultdict
import datetime
import pprint
import os
from collections import defaultdict
import json
from rich import print

# SSL Context docs https://docs.python.org/3/library/ssl.html#ssl.create_default_context

HOST = "imap.fastmail.com"
USERNAME = "klops@fastmail.com"
PASSWORD = "rybvb7c275ywquu3"


class MailMessage:
    def __init__(self, sender, subject, uid):
        self.sender = sender
        self.subject = subject
        self.uid = uid


class AllMessages(dict):
    def __init__(self):
        self.known_subjects = dict()
        super().__init__()

    def rename_and_insert(self, mail: MailMessage):
        desired_name = f"{mail.sender}-{mail.subject}"
        if desired_name not in self:
            self[desired_name] = mail.uid
            self.known_subjects[desired_name] = 0
            return
        self.known_subjects[desired_name] += 1
        self[f"{desired_name}-{self.known_subjects[desired_name]}"] = mail.uid

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


with Imbox(
    HOST,
    username=USERNAME,
    password=PASSWORD,
    ssl=True,
    ssl_context=None,
    starttls=False,
) as imbox:

    all_inbox_messages = imbox.messages()
    mails = set()
    dates = set()
    for uid, message in all_inbox_messages[::]:
        print(message)
        sender = message.sent_from[0]["email"]
        year, month, day = message.parsed_date.strftime("%Y-%m-%d").split("-")

        content = bytes(str(message.body["plain"][0]), encoding="utf_8")
        mail = MailMessage(sender=sender, subject=message.subject[:15], uid=uid)
        mails.add(mail)
        all_messages.rename_and_insert(mail)
        fil_name = all_messages.return_filename(mail.uid)
        dates.add(
            (DateDict(year=year, month=month, day=day, filename=fil_name, uid=uid))
        )
        content_dct[uid] = content
        fil_name_dct[uid] = fil_name

from imapclient import IMAPClient

folder_uid_dct = {}
folders = set()
with IMAPClient(host=HOST) as client:
    client.login(USERNAME, PASSWORD)
    folders_client = client.list_folders()
    print("")
    for f_ in folders_client:
        folder_ = f_[-1]
        folders.add(folder_)
        folder_uid_dct[folder_] = set()
    for folder_ in folders:
        client.select_folder(folder_, readonly=True)
        messages = client.search(["ALL"])
        for uid, message_data in client.fetch(messages, "RFC822").items():
            email_message = email.message_from_bytes(message_data[b"RFC822"])
            # print(f"{folder_=} - {uid} --  {email_message['Message-ID']}")
            folder_uid_dct[folder_].add(uid)
print(folders)
# print(folder_uid_dct)

dates_dict = {}

for date in dates:
    if date.year not in dates_dict:
        dates_dict[date.year] = {}
    if date.month not in dates_dict[date.year]:
        dates_dict[date.year][date.month] = {}
    if date.day not in dates_dict[date.year][date.month]:
        dates_dict[date.year][date.month][date.day] = {}
    if date.filename not in dates_dict[date.year][date.month][date.day]:
        dates_dict[date.year][date.month][date.day][date.filename] = content_dct[
            date.filename
        ]

senders_dict = {}
for mail in mails:
    if mail.sender not in senders_dict:
        senders_dict[mail.sender] = {}
    if mail.uid not in senders_dict[mail.sender]:
        senders_dict[mail.sender][fil_name_dct[mail.uid]] = {}
    if mail.uid not in senders_dict[mail.sender][fil_name_dct[mail.uid]]:
        senders_dict[mail.sender][fil_name_dct[mail.uid]] = content_dct[
            fil_name_dct[mail.uid]
        ]

# folders_dict = {}


def nested_dict():
    """
    Creates a default dictionary where each value is an other default dictionary.
    """
    return defaultdict(nested_dict)


def default_to_regular(d):
    """
    Converts defaultdicts of defaultdicts to dict of dicts.
    """
    if isinstance(d, defaultdict):
        d = {k: default_to_regular(v) for k, v in d.items()}
    return d


def get_path_dict(paths):
    new_path_dict = nested_dict()
    for path in paths:
        parts = path.split("/")
        if parts:
            # marcher = new_path_dict
            for key in parts[:-1]:
                marcher = new_path_dict[key]
                print(f"{parts[-1]}")
                print(f"{path=}")
                marcher[(parts[-1])] = "lol"
                # marcher[(parts[-1])] =  set()

    return default_to_regular(new_path_dict)


print(f"{folders=}")
folders_dict = get_path_dict(folders)
# for folders, uid in folder_uid_dct.items():
#     folders_dict[folders] = uid

pprint.pprint(folders_dict)
# with MailBox(HOST).login(USERNAME, PASSWORD) as mailbox:
#     folders = mailbox.folder.list()  # lists folders in specific mailbox
#     folder_names = [folder["name"] for folder in folders]
#     print(folder_names)
#     folders_dict = get_path_dict(folder_names)


# dates_dict[date.year][date.month][date.day][date.filename] = bytes(str(date.content["plain"][0]), encoding="utf_8")


# pprint.pprint(dates_dict)
