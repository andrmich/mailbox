from pprint import pprint

from rich import print

from mail import mails_dict, senders_dict

def _flatten_dict(dd, separator="/", prefix=""):
    return (
        {
            prefix + separator + str(k) if prefix else k: v
            for kk, vv in dd.items()
            for k, v in _flatten_dict(vv, separator, kk).items()
        }
        if isinstance(dd, dict)
        else {prefix: dd}
    )


def flatten_file_dict(dd):
    path_s = {"/" + str(k): v for k, v in _flatten_dict(dd).items()}
    files_paths = {}
    for key, value in path_s.items():
        files_paths[str(key)] = value
    return files_paths


def get_dirs_to_create(nested: dict, path="/"):
    dirs_to_create = set()
    for k, v in nested.items():
        dirs_to_create.add(path + str(k))
        if isinstance(v, dict):
            new_path = path + str(k) + "/"
            dirs_to_create.update(get_dirs_to_create(v, new_path))
    return dirs_to_create


date_dirs_to_create = get_dirs_to_create(mails_dict)
date_files = flatten_file_dict(mails_dict)

senders_dirs_to_create = get_dirs_to_create(senders_dict)
sender_files = flatten_file_dict(senders_dict)
