
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

