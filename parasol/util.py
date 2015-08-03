
import os.path

def expandpath(path):
    """Expand out a path with both ~ and ENV variables"""
    return os.path.expandvars(os.path.expanduser(path))
