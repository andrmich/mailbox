from typing import Set, Any

from imbox import Imbox
from collections import defaultdict
import datetime
import pprint
import os

# SSL Context docs https://docs.python.org/3/library/ssl.html#ssl.create_default_context

HOST = "imap.fastmail.com"
USERNAME = "klops@fastmail.com"
PASSWORD = "rybvb7c275ywquu3"


class MailMessage:
    def __init__(self, sender, subject, content):
        self.sender = sender
        self.subject = subject
        self.content = content


class AllMessages(dict):
    def __init__(self):
        self.known_subjects = dict()
        super().__init__()

    def rename_and_insert(self, mail: MailMessage):
        desired_name = f"{mail.sender}-{mail.subject}"
        # print(f"{desired_name}")
        if desired_name not in self:
            self[desired_name] = mail.content
            self.known_subjects[desired_name] = 0
            return
        self.known_subjects[desired_name] += 1
        self[f"{desired_name}-{self.known_subjects[desired_name]}"] = mail.content

    def return_filename(self, content=None):
        for key, value in self.items():
            print(f"{key=}")
            print(f"{value=}")
            if value == content:
                return key

class DateDict:
    def __init__(self, year, month, day, filename):
        self.year = year
        self.month = month
        self.day = day
        self.uid = filename

    def __dict__(self):
        return {self.year: {self.month: self.day}}

    def __iter__(self):
        yield from {self.year: {self.month: self.day}}.items()

all_messages = AllMessages()

with Imbox(
    HOST,
    username=USERNAME,
    password=PASSWORD,
    ssl=True,
    ssl_context=None,
    starttls=False,
) as imbox:

    all_inbox_messages = imbox.messages()
    senders = set()
    dates = set()
    folders = set()
    for uid, message in all_inbox_messages[:6]:
        sender = message.sent_from[0]["email"]
        senders.add(sender)
        year, month, day = message.parsed_date.strftime("%Y-%m-%d").split("-")
        uid = uid.decode("utf-8")
        mail = MailMessage(
            sender=sender, subject=message.subject[:15], content=uid
        )
        all_messages.rename_and_insert(mail)
        fil_name = all_messages.return_filename(mail.content)
        # print(f"{fil_name=}")
        dates.add((DateDict(year, month, day, fil_name)))

    status, folders_with_additional_info = imbox.folders()
    for folder in folders_with_additional_info:
        folders.add((folder.split()[-1]).decode("utf-8"))

# print(all_messages)
dates_dict = {}

for date in dates:
    if date.year not in dates_dict:
        dates_dict[date.year] = {}
    if date.month not in dates_dict[date.year]:
        dates_dict[date.year][date.month] = {}
    if date.day not in dates_dict[date.year][date.month]:
        dates_dict[date.year][date.month][date.day] = set()
    dates_dict[date.year][date.month][date.day].add(date.uid)
