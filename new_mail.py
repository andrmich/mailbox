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
    def __init__(self, year, month, day, sender, subject, IMAP_folder):
        self.year = year
        self.month = month
        self.day = day
        self.sender = sender
        self.subject = subject
        self.folder = IMAP_folder

    def __repr__(self):
        return MailMessage.__dict__


class DateDict:
    def __init__(self, year, month, day, uid):
        self.year = year
        self.month = month
        self.day = day
        self.uid = uid

    def __dict__(self):
        return {self.year: {self.month: self.day}}

    def __iter__(self):
        yield from {self.year: {self.month: self.day}}.items()


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
    for uid, message in all_inbox_messages:
        senders.add(message.sent_from[0]["email"])
        print(f"{message.parsed_date=}, {uid=}")
        year, month, day = message.parsed_date.strftime("%Y-%m-%d").split("-")
        uid = uid.decode("utf-8")
        dates.add((DateDict(year, month, day, uid)))

    status, folders_with_additional_info = imbox.folders()
    for folder in folders_with_additional_info:
        folders.add((folder.split()[-1]).decode("utf-8"))

    date_dict = dict.fromkeys([date.year for date in dates])
    for year in date_dict.keys():
        # print(f"{year=}")

        months = set()
        for data in dates:
            if data.year == year:
                months.add(data.month)
                months_dict = defaultdict(set, {k: set() for k in months})

        for month in months:
            days = set()
            for data in dates:
                # print(f"{month=}")
                if data.year == year:
                    if data.month == month:
                        days.add(data.day)
                        days_dict = defaultdict(set, {k: set() for k in days})

            for day in days:
                uids = set()
                for data in dates:
                    if data.year == year:
                        if data.month == month:
                            if data.day == day:
                                uids.add(data.uid)
                days_dict[day] = uids

            months_dict[month] = days_dict
        date_dict[year] = months_dict

pprint.pprint(date_dict)


# if __name__ == '__main__':
#     print(senders)
#     print(dates)
#     print(folders)
#     pprint.pprint(whole_dict)
#     pprint.pprint(dates_dict)
#     pprint.pprint(dates_dict)


dddd = {}
for date in dates:
    if date.year not in dddd:
        dddd[date.year] = {}
    if date.month not in dddd[date.year]:
        dddd[date.year][date.month] = {}
    if date.day not in dddd[date.year][date.month]:
        dddd[date.year][date.month][date.day] = set()
    dddd[date.year][date.month][date.day].add(date.uid)

pprint.pprint(dddd)


def deep_get(_dict, keys, default=None):
    def _reducer(d, key):
        if isinstance(d, dict):
            return d.get(key, default)
        return default
