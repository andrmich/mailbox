from pprint import pprint
from rich import print

from mail import mails_dict, senders_dict

# dates_dict = {
#     "2020": {
#         "03": {"23": {"no-reply@accounts.google.com-Alert bezpiecze": b"324"}},
#         "06": {
#             "02": {"no-reply@accounts.google.com-Alert bezpiecze-1": b"326"},
#             "03": {
#                 "kontakt@best-you.pl-Jutro koniec ak": b"330",
#                 "kontakt@doradca.tv-Zerowe stopy pr": b"325",
#             },
#             "12": {"hello@hyperskill.org-What to do if y": b"313"},
#             "16": {"calendar-notification@google.com-Powiadomienie: ": b"307"},
#             "17": {
#                 "contact@sinsay.com-Ustalenie noweg": b"339",
#                 "help@doyou.com-Hey, is this ri": b"311",
#                 "no-reply@m.mail.coursera.org-Lead for Change": b"336",
#             },
#             "24": {"googleaccount-noreply@google.com-Sabina, sprawdź": b"363"},
#             "28": {"kontakt@doradca.tv-Czy jesteśmy w ": b"275"},
#             "29": {
#                 "no-reply@accounts.google.com-Alert bezpiecze-2": b"354",
#                 "no-reply@accounts.google.com-Alert bezpiecze-3": b"367",
#             },
#             "30": {"kontakt@doradca.tv-W obawie przed ": b"368"},
#         },
#         "07": {
#             "04": {"kontakt@doradca.tv-Skład portfela ": b"369"},
#             "09": {"no-reply@t.mail.coursera.org-Welcome to Cont": b"366"},
#         },
#         "09": {
#             "08": {
#                 "support@fastmail.com-Your import of ": b"370",
#                 "support@fastmail.com-Your import of -1": b"372",
#                 "support@fastmail.com-Your import of -2": b"373",
#             }
#         },
#     },
#     "2021": {
#         "07": {
#             "support@fastmail.com-Your import of ": b"370",
#             "support@fastmail.com-Your import of -1": b"372",
#             "support@fastmail.com-Your import of -2": b"373",
#         },
#         "09": {
#             "08": {
#                 "kontakt@best-you.pl-Jutro koniec ak": b"330",
#                 "kontakt@doradca.tv-Zerowe stopy pr": b"325",
#             },
#             "12": {"hello@hyperskill.org-What to do if y": b"313"},
#         },
#     },
# }
#
# senders_dict = {
#     "calendar-notification@google.com": {
#         "calendar-notification@google.com-Powiadomienie: ": b"307"
#     },
#     "contact@sinsay.com": {"contact@sinsay.com-Ustalenie noweg": b"339"},
#     "googleaccount-noreply@google.com": {
#         "googleaccount-noreply@google.com-Sabina, sprawdź": b"363"
#     },
#     "hello@hyperskill.org": {"hello@hyperskill.org-What to do if y": b"313"},
#     "help@doyou.com": {"help@doyou.com-Hey, is this ri": b"311"},
#     "kontakt@best-you.pl": {"kontakt@best-you.pl-Jutro koniec ak": b"330"},
#     "kontakt@doradca.tv": {
#         "kontakt@doradca.tv-Czy jesteśmy w ": b"275",
#         "kontakt@doradca.tv-Skład portfela ": b"369",
#         "kontakt@doradca.tv-W obawie przed ": b"368",
#         "kontakt@doradca.tv-Zerowe stopy pr": b"325",
#     },
#     "no-reply@accounts.google.com": {
#         "no-reply@accounts.google.com-Alert bezpiecze": b"324",
#         "no-reply@accounts.google.com-Alert bezpiecze-1": b"326",
#         "no-reply@accounts.google.com-Alert bezpiecze-2": b"354",
#         "no-reply@accounts.google.com-Alert bezpiecze-3": b"367",
#     },
#     "no-reply@m.mail.coursera.org": {
#         "no-reply@m.mail.coursera.org-Lead for Change": b"336"
#     },
#     "no-reply@t.mail.coursera.org": {
#         "no-reply@t.mail.coursera.org-Welcome to Cont": b"366"
#     },
#     "support@fastmail.com": {
#         "support@fastmail.com-Your import of ": b"370",
#         "support@fastmail.com-Your import of -1": b"372",
#         "support@fastmail.com-Your import of -2": b"373",
#     },
# }


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
    # print(dd)
    # print()
    path_s = {"/" + str(k): v for k, v in _flatten_dict(dd).items()}
    # print(path_s)
    files_paths = {}
    for key, value in path_s.items():
        files_paths[str(key)] = value

    # print(f"{files_paths=}")
    return files_paths


def get_dirs_to_create(nested: dict, path="/"):
    dirs_to_create = set()
    for k, v in nested.items():
        # print(f"{k=}")
        # print(f"{v=}")
        dirs_to_create.add(path + str(k))
        if isinstance(v, dict):
            new_path = path + str(k) + "/"
            dirs_to_create.update(get_dirs_to_create(v, new_path))
    return dirs_to_create


date_dirs_to_create = get_dirs_to_create(mails_dict)
date_files = flatten_file_dict(mails_dict)

senders_dirs_to_create = get_dirs_to_create(senders_dict)
sender_files = flatten_file_dict(senders_dict)

# print(senders_dirs_to_create)
# pprint(f"{date_dirs_to_create=}")
# pprint(f"{date_files=}")
# pprint(f"{senders_dirs_to_create=}")
# pprint(f"{sender_files=}")