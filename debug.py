"""Import debug to allow postmortem debugging.

"""
import sys


def exchook(type_, value, tb):
    import traceback
    import ipdb
    traceback.print_exception(type_, value, tb)
    ipdb.pm()


def setup_exchook():
    sys.excepthook = exchook
