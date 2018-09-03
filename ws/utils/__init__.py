import os

def get_parent_paths(path, stop_at):
    """ get parent paths up to stop_at. includes the current path, and stop_at """
    assert stop_at in path
    if stop_at not in path:
        return []

    path = os.path.expanduser(path)

    ps = [os.path.abspath(path)]
    while True:
        path = os.path.abspath(os.path.join(path, os.pardir))
        ps.append(path)
        if path == stop_at:
            break

    return ps