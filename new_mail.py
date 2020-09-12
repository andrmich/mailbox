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
    def __init__(self, year, month, day, filename, content):
        self.year = year
        self.month = month
        self.day = day
        self.filename = filename
        self.content = content

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
    for uid, message in all_inbox_messages[:4]:
        sender = message.sent_from[0]["email"]
        senders.add(sender)
        year, month, day = message.parsed_date.strftime("%Y-%m-%d").split("-")
        uid = uid.decode("utf-8")
        mail = MailMessage(sender=sender, subject=message.subject[:15], uid=uid)
        all_messages.rename_and_insert(mail)
        fil_name = all_messages.return_filename(mail.uid)
        content = message.body
        dates.add(
            (
                DateDict(
                    year=year, month=month, day=day, filename=fil_name, content=content
                )
            )
        )

    status, folders_with_additional_info = imbox.folders()
    for folder in folders_with_additional_info:
        folders.add((folder.split()[-1]).decode("utf-8"))

dates_dict = {}

for date in dates:
    print(f"{date.filename=}")
    print(f"{date.content['plain']}")
    print(len(date.content["plain"]))
    if date.year not in dates_dict:
        dates_dict[date.year] = {}
    if date.month not in dates_dict[date.year]:
        dates_dict[date.year][date.month] = {}
    if date.day not in dates_dict[date.year][date.month]:
        dates_dict[date.year][date.month][date.day] = {}
    if date.filename not in dates_dict[date.year][date.month][date.day]:
        dates_dict[date.year][date.month][date.day][date.filename] = bytes(str(date.content["plain"][0]), encoding="utf_8")

# pprint.pprint(dates_dict)
