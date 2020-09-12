import errno
import os
import sys
from collections import defaultdict
from stat import S_IFDIR, S_IFREG
from time import time

from fuse import FUSE, Operations, FuseOSError
import new_mail
import pprint


class MyStat:
    def __init__(self):
        self.st_mode = S_IFDIR | 0o0755
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 2
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 4096
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0


class Passthrough(Operations):
    def __init__(self, root):
        self.root = root
        self.files = {}
        self.data = defaultdict(bytes)
        # self.data = new_mail.date_dict
        self.fd = 0
        now = time()
        self.files["/"] = dict(
            st_mode=(S_IFDIR | 0o755),
            st_ctime=now,
            st_mtime=now,
            st_atime=now,
            st_nlink=2,
        )
        self.dirs = {}
        for key, value in new_mail.dates_dict.items():
            self.dirs[key] = dict(
                st_mode=(S_IFDIR | 0o755),
                st_ctime=now,
                st_mtime=now,
                st_atime=now,
                st_nlink=2,
            )
            print(key)
            print(new_mail.dates_dict["2020"])
            for k, v in new_mail.dates_dict[key]:
                self.dirs[k] = dict(
                    st_mode=(S_IFDIR | 0o755),
                    st_ctime=now,
                    st_mtime=now,
                    st_atime=now,
                    st_nlink=2,
                )
                print(k)

        # for key in self.files.keys():
        # self.files['/2020'] = dict(
        # st_mode=(S_IFDIR | 0o755),
        # st_ctime=now,
        # st_mtime=now,
        # st_atime=now,
        # st_nlink=2)
        # self.files['/2020/proba'] = dict(
        # st_mode=(S_IFDIR | 0o755),
        # st_ctime=now,
        # st_mtime=now,
        # st_atime=now,
        # st_nlink=2)

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]

        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode=os.R_OK):
        print(f"access({path=}, {mode=})")
        mode_t = os.R_OK
        full_path = self._full_path(path)
        if not os.access(full_path, mode=mode_t):
            raise FuseOSError(errno.EACCES)

    # def chmod(self, path, mode):
    #     print(f"chmod {path=}, {mode=}")
    #     full_path = self._full_path(path)
    #     return os.chmod(full_path, mode)

    def chmod(self, path, mode):
        self.files[path]["st_mode"] &= 0o770000
        self.files[path]["st_mode"] |= mode
        return 0

    def chown(self, path, uid, gid):
        print(f"chown {path=}, {uid=}, {gid=}")
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    # def getattr(self, path, fh=None):
    #     print(f"getattr({path=}, {fh=})")
    #     aaa = {
    #         "st_atime": 1,
    #         "st_ctime": 1,
    #         "st_gid": 1000,
    #         "st_mode": 33444,
    #         "st_mtime": 1,
    #         "st_nlink": 1,
    #         "st_size": 123,
    #         "st_uid": 1000,
    #         "st_blocks": 1,
    #     }
    #     bbb = {
    #         "st_atime": 1599500384.7839124,
    #         "st_ctime": 1599500384.7839124,
    #         "st_gid": 1000,
    #         "st_mode": 33444,
    #         "st_mtime": 1599500384.7839124,
    #         "st_nlink": 1,
    #         "st_size": 0,
    #         "st_uid": 1000,
    #         "st_blocks": 1,
    #     }
    #     # return bbb
    #     full_path = self._full_path(path)
    #     st = os.lstat(full_path)
    #     pprint.pprint(f"{st=}")
    #     d = dict(
    #         (key, getattr(st, key))
    #         for key in (
    #             "st_atime",
    #             "st_ctime",
    #             "st_gid",
    #             "st_mode",
    #             "st_mtime",
    #             "st_nlink",
    #             "st_size",
    #             "st_uid",
    #             "st_blocks",
    #         )
    #     )
    #     print(d)
    #     return d

    def getattr(self, path, fh=None):
        if path not in self.files:
            raise FuseOSError(errno.ENOENT)

        return self.files[path]

    def create(self, path, mode, fi=None):
        self.files[path] = dict(
            st_mode=(S_IFREG | mode),
            st_nlink=1,
            st_size=0,
            st_ctime=time(),
            st_mtime=time(),
            st_atime=time(),
        )

        self.fd += 1
        return self.fd

    # def readdir(self, path, fh):
    #     full_path = self._full_path(path)
    #
    #     dirents = ['.', '..']
    #     if os.path.isdir(full_path):
    #         dirents.extend(os.listdir(full_path))
    #     for r in dirents:
    #         yield r

    # def readdir(self, path, fh):
    #     print("readdir", path)
    #     dirents = [".", ".."]
    #     if path == "/":
    #         dirents.append([new_mail.date_dict.keys()])
    #     else:
    #         dirents.extend([new_mail.date_dict.keys()])
    #     for r in dirents:
    #         yield r

    # def readdir(self, path, fh):
    #     print(f"readdir({path=}, {fh=})")
    #     for x in new_mail.date_dict.keys():
    #         yield x
    #         return
    #     full_path = self._full_path(path)
    #
    #     dirents = [".", ".."]
    #     dirents.append(new_mail.date_dict.keys())
    #     if os.path.isdir(full_path):
    #         dirents.extend(os.listdir(full_path))
    #     for r in dirents:
    #         print(r)
    #         yield r
    def readdir(self, path, fh):
        return [".", ".."] + [x for x in self.dirs.keys() if x != "/"]

    def readlink(self, path):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    # def mkdir(self, path, mode):
    #     return os.mkdir(self._full_path(path), mode)

    def mkdir(self, path, mode):
        self.files[path] = dict(
            st_mode=(S_IFDIR | mode),
            st_nlink=2,
            st_size=0,
            st_ctime=time(),
            st_mtime=time(),
            st_atime=time(),
        )

        self.files["/"]["st_nlink"] += 1

    def statfs(self, path):
        print(f"statfd {path=}")
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        print(f"{stv=}")
        return dict(
            (key, getattr(stv, key))
            for key in (
                "f_bavail",
                "f_bfree",
                "f_blocks",
                "f_bsize",
                "f_favail",
                "f_ffree",
                "f_files",
                "f_flag",
                "f_frsize",
                "f_namemax",
            )
        )

    def unlink(self, path):
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        return os.symlink(name, self._full_path(target))

    def rename(self, old, new):
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        return os.link(self._full_path(target), self._full_path(name))

    def utimens(self, path, times=None):
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        with open(full_path, "r+") as f:
            f.truncate(length)

    def flush(self, path, fh):
        return os.fsync(fh)

    def release(self, path, fh):
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        print(f"fsync {path=}, {fdatasync=}, {fh=}")
        return self.flush(path, fh)


def main(mountpoint, root):
    FUSE(
        Passthrough(root),
        mountpoint,
        nothreads=True,
        foreground=True,
        **{"allow_other": True},
    )


if __name__ == "__main__":
    print("RELOADING NOW")
    mountpoint = sys.argv[2]
    root = sys.argv[1]
    main(mountpoint, root)
