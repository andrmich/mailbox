import json
import os
import pprint
from uuid import uuid4

from directory_tree import flatten_file_dict, get_dirs_to_create
from imap_tools import MailBox
from rich import inspect, print
from tqdm import tqdm

HOST = "imap.fastmail.com"
USERNAME = "klops@fastmail.com"
PASSWORD = "rybvb7c275ywquu3"
# USERNAME = os.environ["MAILBOX_USERNAME"]
# PASSWORD = os.environ["MAILBOX_PASSWORD"]


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


def create_topics(mbox):
    folders_mailbox = mbox.folder.list()
    return [folder["name"] for folder in folders_mailbox]


def create_mail_obj(message, filename_generator):
    mail_ = MailMessage(
        sender=message.from_,
        subject=message.subject[:10],
        year=str(message.date.year),
        month=str(message.date.month),
        day=str(message.date.day),
        content=bytes(message.html, encoding="utf-8"),
    )
    mail_.filename = filename_generator.get_filename(mail_)
    return mail_


with MailBox(HOST).login(USERNAME, PASSWORD) as mailbox:
    filename_generator = FilenameGenerator()
    mails = set()
    folders_dict = dict.fromkeys(create_topics(mailbox))
    for folder_name in tqdm(folders_dict.keys()):
        folders_dict[folder_name] = set()
        mailbox.folder.set(folder_name)
        for msg in mailbox.fetch():
            mail_obj = create_mail_obj(msg, filename_generator)
            mails.add(mail_obj)  # creates set of all messages in mailbox
            folders_dict[folder_name].add(mail_obj)


def create_topic_dir(tpc_dct):
    topics_dict = {f"/{key}": value for key, value in tpc_dct.items()}
    return topics_dict


def create_timeline_dir(all_mails):
    mails_dict = {}
    for mail in all_mails:
        if mail.year not in mails_dict:
            mails_dict[mail.year] = {}
        if mail.month not in mails_dict[mail.year]:
            mails_dict[mail.year][mail.month] = {}
        if mail.day not in mails_dict[mail.year][mail.month]:
            mails_dict[mail.year][mail.month][mail.day] = {}
        if mail not in mails_dict[mail.year][mail.month][mail.day]:
            mails_dict[mail.year][mail.month][mail.day][mail.filename] = mail.content
    return mails_dict


def create_sender_dir(all_mails):
    senders_dict = {}
    for mail in all_mails:
        if mail.sender not in senders_dict:
            senders_dict[mail.sender] = {}
        if mail not in senders_dict[mail.sender]:
            senders_dict[mail.sender][mail.filename] = mail.content
    return senders_dict


def create_dirs(all_mails, tcp_dct):
    mails_dict = create_timeline_dir(all_mails)
    senders_dict = create_sender_dir(all_mails)
    topic_dict = create_topic_dir(tcp_dct)
    return mails_dict, senders_dict, topic_dict


date_dirs_to_create_set = get_dirs_to_create(create_timeline_dir(mails))
date_files = flatten_file_dict(create_timeline_dir(mails))
date_dirs_to_create = date_dirs_to_create_set - date_files.keys()

senders_dirs_to_create_set = get_dirs_to_create(create_sender_dir(mails))
sender_files = flatten_file_dict(create_sender_dir(mails))
senders_dirs_to_create = senders_dirs_to_create_set - sender_files.keys()

topics_dict = create_topic_dir(folders_dict)
