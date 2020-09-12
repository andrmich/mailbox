#!/usr/bin/env python
from __future__ import print_function, absolute_import, division
import os
import types
import inspect

from typing import Dict, cast
import logging

from rich import print
from rich import inspect as rich_inspect

from collections import defaultdict
from errno import ENOENT
from stat import S_IFDIR, S_IFLNK, S_IFREG
from time import time

from fuse import FUSE, Operations, LoggingMixIn


class FuseOSError(OSError):
    def __init__(self, errno, filename=None):
        super(FuseOSError, self).__init__(errno, os.strerror(errno), filename)


if not hasattr(__builtins__, "bytes"):
    bytes = str


class PseudoFile(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.isdir = False


class Directory(PseudoFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.isdir = True


class Memory(Operations):
    "Example memory filesystem. Supports only one level of files."

    def __init__(self):
        self.files: Dict[str, PseudoFile] = {}
        self.data = defaultdict(bytes)
        self.fd = 0
        now = time()
        self.files["/"] = Directory(
            st_mode=(S_IFDIR | 0o755),
            st_ctime=now,
            st_mtime=now,
            st_atime=now,
            st_nlink=2,
        )

    def chmod(self, path, mode):
        this_function_name = cast(
            types.FrameType, inspect.currentframe()
        ).f_code.co_name
        print(this_function_name)
        self.files[path]["st_mode"] &= 0o770000
        self.files[path]["st_mode"] |= mode
        return 0

    def chown(self, path, uid, gid):
        this_function_name = cast(
            types.FrameType, inspect.currentframe()
        ).f_code.co_name
        print(this_function_name)
        self.files[path]["st_uid"] = uid
        self.files[path]["st_gid"] = gid

    def create(self, path, mode):
        self.files[path] = PseudoFile(
            st_mode=(S_IFREG | mode),
            st_nlink=1,
            st_size=0,
            st_ctime=time(),
            st_mtime=time(),
            st_atime=time(),
        )

        self.fd += 1
        print(f"create({path=}, {mode=})\n{self.files}")
        rich_inspect(self)
        return self.fd

    def getattr(self, path, fh=None):
        print(f"getattr({path=}, {fh=})")
        if path not in self.files:
            raise FuseOSError(ENOENT, filename=path)

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
        this_function_name = cast(
            types.FrameType, inspect.currentframe()
        ).f_code.co_name
        print(this_function_name)
        self.files[path] = Directory(
            st_mode=(S_IFDIR | mode),
            st_nlink=2,
            st_size=0,
            st_ctime=time(),
            st_mtime=time(),
            st_atime=time(),
        )

        self.files["/"]["st_nlink"] += 1

    def open(self, path, flags):
        this_function_name = cast(
            types.FrameType, inspect.currentframe()
        ).f_code.co_name
        print(this_function_name)
        self.fd += 1
        return self.fd

    def read(self, path, size, offset, fh):
        this_function_name = cast(
            types.FrameType, inspect.currentframe()
        ).f_code.co_name
        print(this_function_name)
        return self.data[path][offset : offset + size]

    def readdir(self, path, fh):
        print(f"readdir({path=}, {fh=}")
        if not self.files[path].isdir:
            print("This is not a directory!")
        files_inside = {
            k: v for k, v in self.files.items() if k.startswith(path) and k != path
        }
        print(f"{files_inside=}")
        return_value = [".", ".."] + [
            x[len(path) :].lstrip("/") for x in files_inside if x != path
        ]
        return_value = [x for x in return_value if "/" not in x]
        print(f"{return_value}")
        return return_value

    def readlink(self, path):
        this_function_name = cast(
            types.FrameType, inspect.currentframe()
        ).f_code.co_name
        print(this_function_name)
        return self.data[path]

    def removexattr(self, path, name):
        this_function_name = cast(
            types.FrameType, inspect.currentframe()
        ).f_code.co_name
        print(this_function_name)
        attrs = self.files[path].get("attrs", {})

        try:
            del attrs[name]
        except KeyError:
            pass  # Should return ENOATTR

    def rename(self, old, new):
        this_function_name = cast(
            types.FrameType, inspect.currentframe()
        ).f_code.co_name
        print(this_function_name)
        self.data[new] = self.data.pop(old)
        self.files[new] = self.files.pop(old)

    def rmdir(self, path):
        this_function_name = cast(
            types.FrameType, inspect.currentframe()
        ).f_code.co_name
        print(this_function_name)
        # with multiple level support, need to raise ENOTEMPTY if contains any files
        self.files.pop(path)
        self.files["/"]["st_nlink"] -= 1

    def setxattr(self, path, name, value, options, position=0):
        this_function_name = cast(
            types.FrameType, inspect.currentframe()
        ).f_code.co_name
        print(this_function_name)
        # Ignore options
        attrs = self.files[path].setdefault("attrs", {})
        attrs[name] = value

    def statfs(self, path):
        this_function_name = cast(
            types.FrameType, inspect.currentframe()
        ).f_code.co_name
        print(this_function_name)
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)

    def symlink(self, target, source):
        this_function_name = cast(
            types.FrameType, inspect.currentframe()
        ).f_code.co_name
        print(this_function_name)
        self.files[target] = dict(
            st_mode=(S_IFLNK | 0o777), st_nlink=1, st_size=len(source)
        )

        self.data[target] = source

    def truncate(self, path, length, fh=None):
        this_function_name = cast(
            types.FrameType, inspect.currentframe()
        ).f_code.co_name
        print(this_function_name)
        # make sure extending the file fills in zero bytes
        self.data[path] = self.data[path][:length].ljust(length, "\x00".encode("ascii"))
        self.files[path]["st_size"] = length

    def unlink(self, path):
        this_function_name = cast(
            types.FrameType, inspect.currentframe()
        ).f_code.co_name
        print(this_function_name)
        self.data.pop(path)
        self.files.pop(path)

    def utimens(self, path, times=None):
        this_function_name = cast(
            types.FrameType, inspect.currentframe()
        ).f_code.co_name
        print(this_function_name)
        now = time()
        atime, mtime = times if times else (now, now)
        self.files[path]["st_atime"] = atime
        self.files[path]["st_mtime"] = mtime

    def write(self, path, data, offset, fh):
        this_function_name = cast(
            types.FrameType, inspect.currentframe()
        ).f_code.co_name
        print(this_function_name)
        self.data[path] = (
            # make sure the data gets inserted at the right offset
            self.data[path][:offset].ljust(offset, "\x00".encode("ascii"))
            + data
            # and only overwrites the bytes that data is replacing
            + self.data[path][offset + len(data) :]
        )
        self.files[path]["st_size"] = len(self.data[path])
        return len(data)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("mount")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    fuse = FUSE(Memory(), args.mount, foreground=True, allow_other=True)
