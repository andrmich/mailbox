from pprint import pprint

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
    # pprint(dd)
    print()
    path_s = {"/" + k: v for k, v in _flatten_dict(dd).items()}
    pprint(path_s)
    elem = {}
    for k, v in path_s.items():
        for mail in v:
            elem[k + "/" + mail] = "content"
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

if __name__ == "__main__":
    # sil(6)
    # iterdict(dct)
    print(elem)

    # print(get_dirs_to_create(dct))
