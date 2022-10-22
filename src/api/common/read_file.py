import os
import sys


def read_file(filename, mode='r'):
    try:
        with open(os.path.expanduser(filename), mode) as f:
            return f.read()
    except IOError as e:
        print(e)
        sys.exit()
    except (LookupError, UnicodeDecodeError, UnicodeError) as e:
        print(e)
        sys.exit()
