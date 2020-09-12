# from pprint import pprint
from rich import print

from new_mail import dates_dict

# dates_dict = {
#     "2020": {
#         "03": {"23": {"324"}},
#         "06": {
#             "02": {"326"},
#             "03": {"325", "330"},
#             "12": {"313"},
#             "16": {"307"},
#             "17": {"311", "339", "336"},
#             "24": {"363"},
#             "28": {"275"},
#             "29": {"367", "354"},
#             "30": {"368"},
#         },
#         "07": {"04": {"369"}, "09": {"366"}},
#         "09": {"08": {"370", "372", "373"}},},
#     "2021": {
#         "03": {"23": {"324"}},
#         "06": {
#             "02": {"326"},
#             "03": {"325", "330"},
#             "12": {"313"},
#         },
#     }
# }
# dates_dict = {
#     "2020": {
#         "03": {
#             "23": {"no-reply@accounts.google.com-Alert bezpiecze": ["fileconent23"]}
#         },
#         "06": {
#             "02": {"no-reply@accounts.google.com-Alert bezpiecze-1": ["fileconent02"]},
#             "03": {
#                 "kontakt@best-you.pl-Jutro koniec ak": ["fileconent03"],
#                 "kontakt@doradca.tv-Zerowe stopy pr": ["fileconent03"],
#             },
#             "12": {"hello@hyperskill.org-What to do if y": ["fileconent03"]},
#             "16": {
#                 "calendar-notification@google.com-Powiadomienie: ": ["fileconent03"]
#             },
#             "17": {
#                 "contact@sinsay.com-Ustalenie noweg": ["fileconent03"],
#                 "help@doyou.com-Hey, is this ri": ["fileconent03"],
#             },
#             "no-reply@m.mail.coursera.org-Lead for Change": ["fileconent03"],
#         },
#         "24": {"googleaccount-noreply@google.com-Sabina, sprawdź": ["fileconent03"]},
#         "28": {"kontakt@doradca.tv-Czy jesteśmy w ": ["fileconent03"]},
#         "29": {
#             "no-reply@accounts.google.com-Alert bezpiecze-2": ["fileconent03"],
#             "no-reply@accounts.google.com-Alert bezpiecze-3": ["fileconent03"],
#         },
#         "30": {"kontakt@doradca.tv-W obawie przed ": ["fileconent03"]},
#     },
#     "07": {
#         "04": {"kontakt@doradca.tv-Skład portfela ": ["fileconent03"]},
#         "09": {"no-reply@t.mail.coursera.org-Welcome to Cont": ["fileconent03"]},
#     },
#     "09": {
#         "08": {
#             "support@fastmail.com-Your import of ": ["fileconent03"],
#             "support@fastmail.com-Your import of -1": ["fileconent03"],
#             "support@fastmail.com-Your import of -2": ["fileconent03"],
#         },
#     },
#     "2021": {
#         "07": {
#             "04": {"kontakt@doradca.tv-Skład portfela ": ["fileconent03"]},
#             "09": {"no-reply@t.mail.coursera.org-Welcome to Cont": ["fileconent03"]},
#         },
#         "09": {
#             "08": {
#                 "support@fastmail.com-Your import of ": ["fileconent03"],
#                 "support@fastmail.com-Your import of -1": ["fileconent03"],
#                 "support@fastmail.com-Your import of -2": ["fileconent03"],
#             }
#         },
#     },
# }


def _flatten_dict(dd, separator="/", prefix=""):
    return (
        {
            prefix + separator + k if prefix else k: v
            for kk, vv in dd.items()
            for k, v in _flatten_dict(vv, separator, kk).items()
        }
        if isinstance(dd, dict)
        else {prefix: dd}
    )


def flatten_file_dict(dd):
    # print(dd)
    # print()
    path_s = {"/" + k: v for k, v in _flatten_dict(dd).items()}
    # print(path_s)
    elem = {}
    for key, value in path_s.items():
        elem[key] = value

    print(f"{elem=}")
    return elem


def get_dirs_to_create(nested: dict, path="/"):
    dirs_to_create = set()
    for k, v in nested.items():
        dirs_to_create.add(path + k)
        if isinstance(v, dict):
            new_path = path + k + "/"
            dirs_to_create.update(get_dirs_to_create(v, new_path))
    return dirs_to_create




dirs_to_create = get_dirs_to_create(dates_dict)
elem = flatten_file_dict(dates_dict)
elem_keys = flatten_file_dict(dates_dict).keys()

set_dirs_to_create = dirs_to_create - set(elem_keys)