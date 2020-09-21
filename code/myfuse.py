#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

import inspect
import os
import types
from collections import defaultdict
from errno import ENOENT, EPERM
from time import time
from typing import cast

from fuse import Operations
from rich import print

DIR_DCT = {
    "st_mode": 16877,
    "st_ctime": 1599908032.1020591,
    "st_mtime": 1599908032.1020591,
    "st_atime": 1599908032.1020591,
    "st_nlink": 2,
}

FILE_DCT = {
    "st_mode": 33188,
    "st_nlink": 1,
    "st_size": 0,
    "st_ctime": 1599908285.62782,
    "st_mtime": 1599908285.6278203,
    "st_atime": 1599908285.6278203,
}


class FuseOSError(OSError):
    def __init__(self, errno, filename=None):
        super().__init__(errno, os.strerror(errno), filename)


class PseudoFile(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.isdir = False


class Directory(PseudoFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.isdir = True


def create_main_dir_tree():
    return {
        "/": Directory(DIR_DCT),
        "/timeline": Directory(DIR_DCT),
        "/sender": Directory(DIR_DCT),
        "/topics": Directory(DIR_DCT),
    }


class Memory(Operations):
    """ Memory filesystem operations. Read-only."""

    def __init__(
        self,
        date_dirs_to_create,
        date_files,
        topics_dict,
        senders_dirs_to_create,
        sender_files,
    ):
        self.files = {}
        self.data = defaultdict(bytes)
        self.fd = 0
        self.files = create_main_dir_tree()
        self._create_timeline_dir_tree(date_dirs_to_create, date_files)
        self._create_sender_dir_tree(senders_dirs_to_create, sender_files)
        self._create_topics_dir_tree(topics_dict)

    def _create_timeline_dir_tree(self, date_dirs_to_create, date_files):
        for key in date_dirs_to_create:
            self.files[f"/timeline{key}"] = Directory(DIR_DCT)
        for key, value in date_files.items():
            self.files[f"/timeline{key}.html"] = PseudoFile(FILE_DCT)
            self.data[f"/timeline{key}.html"] = value

    def _create_topics_dir_tree(self, topics_dict):
        for key, value in topics_dict.items():
            self.files[f"/topics{key}"] = Directory(DIR_DCT)
            for mail in value:
                self.files[f"/topics{key}/{mail.filename}.html"] = PseudoFile(FILE_DCT)
                self.data[f"/topics{key}/{mail.filename}.html"] = mail.content

    def _create_sender_dir_tree(self, senders_dirs_to_create, sender_files):
        for key in senders_dirs_to_create:
            self.files[f"/sender{key}"] = Directory(DIR_DCT)
        for key, value in sender_files.items():
            self.files[f"/sender{key}.html"] = PseudoFile(FILE_DCT)
            self.data[f"/sender{key}.html"] = value

    def chmod(self, path, mode):
        raise FuseOSError(EPERM)

    def chown(self, path, uid, gid):
        raise FuseOSError(EPERM)

    def create(self, path, mode):
        raise FuseOSError(EPERM)

    def getattr(self, path, fh=None):
        print(f"getattr({path=}, {fh=})")
        if path not in self.files:
            raise FuseOSError(ENOENT, filename=path)
        if path in self.data:
            self.files[path]["st_size"] = len(self.data[path])
        return self.files[path]

    def getxattr(self, path, name, position=0):
        print(f"getxattr({path=}, {name=}, {position=})")
        attrs = self.files[path].get("attrs", {})

        try:
            return attrs[name]
        except KeyError:
            return ""  # Should return ENOATTR

    def listxattr(self, path):
        this_function_name = cast(
            types.FrameType, inspect.currentframe()
        ).f_code.co_name
        print(this_function_name)
        attrs = self.files[path].get("attrs", {})
        return attrs.keys()

    def mkdir(self, path, mode):
        raise FuseOSError(EPERM)

    def open(self, path, flags):
        self.fd += 1
        return self.fd

    def read(self, path, size, offset, fh):
        return self.data[path]

    def readdir(self, path, fh):
        files_inside = {
            k: v for k, v in self.files.items() if k.startswith(path) and k != path
        }
        short_dir = list(
            set(
                [
                    (k[len(path) :].lstrip("/")).split("/")[0]
                    for k in files_inside.keys()
                    if k != path
                ]
            )
        )
        return_value = [".", ".."] + short_dir
        return_value = [x for x in return_value if "/" not in x]
        print(f"{return_value}")
        return return_value

    def readlink(self, path):
        return self.data[path]

    def removexattr(self, path, name):
        raise FuseOSError(EPERM)

    def rename(self, old, new):
        raise FuseOSError(EPERM)

    def rmdir(self, path):
        raise FuseOSError(EPERM)

    def setxattr(self, path, name, value, options, position=0):
        raise FuseOSError(EPERM)

    def statfs(self, path):
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)

    def symlink(self, target, source):
        raise FuseOSError(EPERM)

    def truncate(self, path, length, fh=None):
        raise FuseOSError(EPERM)

    def unlink(self, path):
        raise FuseOSError(EPERM)

    def utimens(self, path, times=None):
        raise FuseOSError(EPERM)

    def write(self, path, data, offset, fh):
        raise FuseOSError(EPERM)
