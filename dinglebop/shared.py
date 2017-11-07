"""Shared functionalities for the dinglebop package."""

import os


HOMEDIR = os.path.expanduser("~")
dinglebop_DIR_NAME = '.dinglebop'
dinglebop_DIR_PATH = os.path.join(HOMEDIR, dinglebop_DIR_NAME)
os.makedirs(dinglebop_DIR_PATH, exist_ok=True)
