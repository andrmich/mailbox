import logging

from fuse import FUSE

from directory_tree import get_dirs_to_create, flatten_file_dict
from mail import (
    fetch_folders_and_mails, create_timeline_dir, create_sender_dir, create_topic_dir)
from myfuse import Memory

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("mount")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    folders_dict, mails = fetch_folders_and_mails()
    date_dirs_to_create_set = get_dirs_to_create(create_timeline_dir(mails))
    date_files = flatten_file_dict(create_timeline_dir(mails))
    date_dirs_to_create = date_dirs_to_create_set - date_files.keys()

    senders_dirs_to_create_set = get_dirs_to_create(create_sender_dir(mails))
    sender_files = flatten_file_dict(create_sender_dir(mails))
    senders_dirs_to_create = senders_dirs_to_create_set - sender_files.keys()

    topics_dict = create_topic_dir(folders_dict)


    fuse = FUSE(
        Memory(
            date_dirs_to_create=date_dirs_to_create,
            senders_dirs_to_create=senders_dirs_to_create,
            topics_dict=topics_dict,
            sender_files=sender_files,
            date_files=date_files,
        ),
        args.mount,
        foreground=True,
        allow_other=True,
    )
