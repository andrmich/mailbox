from collections import defaultdict

from imap_tools import MailBox, AND
import pprint
from sqlalchemy import create_engine

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

    def __repr__(self):
        pass

    def create_email_object(self):
        pass

    def years(self):
        years = list(self.__dict__.values())[0]
        return years


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
    messages_dict_sender = defaultdict(set)
    messages_dict_folders = defaultdict(set)
    senders = set()
    folders = set()
    for folder_name in folder_names:
        mailbox.folder.set(folder_name)
        for msg in mailbox.fetch():
            year = msg.date.year
            month = msg.date.month
            day = msg.date.day
            sender = msg.from_
            subject = msg.subject[:20]
            element = MailMessage(
                year=year,
                month=month,
                day=day,
                sender=sender,
                subject=subject,
                IMAP_folder=folder_name,
            )
            all_messages.rename_and_insert(element)
            # for key, value in all_messages.items():
            #     if value == element:
            #         yield key
            # name = all_messages[element]
            # senders.add(element.sender)
            # folders.add(element.folder)
            # for sender in senders:

            # messages_dict_sender = dict.fromkeys(senders)
            # print(messages_dict_sender)
            # messages_dict_sender[sender].add(name)
            # messages_dict_sender[folder_name].add(name)

            # messages_dict_folders = dict.fromkeys(folders)
            # messages_dict_folders[f"{element.folder}"].add(name)

    # whole_dict = {"sender": messages_dict_sender, "timeline": messages_dict_folders}
    # messages_dict["timeline"].add(f"{year}-{name}")
    #
    # # messages_dict["timeline"][f"{year}"].add(month)
    # messages_dict["sender"].add(sender)
    # messages_dictes_dict["topics"].add(folder_name)

    #     if str(month) not in messages_dict["timeline"]["year"].values():
    #         messages_dict["timeline"]["year"] = str(month)
    #         if str(day) not in messages_dict["timeline"]["year"]["month"]:
    #             messages_dict["timeline"]["year"]["month"] = str(day)
    # messages_dict["timeline"]["year"]["month"]["day"] = all_messages["desired_name"]


if __name__ == "__main__":
    # print(set(mhs))
    # pprint.pprint(all_messagesgs.values().__dict__['month'])
    pprint.pprint(all_messages)
