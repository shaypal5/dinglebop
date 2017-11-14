"""Shared functionalities for the dinglebop package."""

import os
import json


HOMEDIR = os.path.expanduser("~")
DINGLEBOP_DIR_NAME = '.dinglebop'
DINGLEBOP_DIR_PATH = os.path.join(HOMEDIR, DINGLEBOP_DIR_NAME)
os.makedirs(DINGLEBOP_DIR_PATH, exist_ok=True)

DINGLEBOP_CFG_FNAME = 'dinglebop_cfg.json'
DINGLEBOP_CFG_FPATH = os.path.join(DINGLEBOP_DIR_PATH, DINGLEBOP_CFG_FNAME)

CACHE_DIR_NAME = 'cache'
CACHE_DIR_PATH = os.path.join(DINGLEBOP_DIR_PATH, CACHE_DIR_NAME)
os.makedirs(CACHE_DIR_PATH, exist_ok=True)


MISSING_CONF_FILE_MSG = (
    "The mandatory dinglebop configuration file is missing from the expected "
    "path: {}. Please create the missing file with configuration information."
)


def get_dinglebop_cfg():
    """Returns the dinglebop configuration mapping."""
    try:
        with open(DINGLEBOP_CFG_FPATH, 'r') as cfgfile:
            return json.load(cfgfile)
    except FileNotFoundError:
        raise FileNotFoundError(
            MISSING_CONF_FILE_MSG.format(DINGLEBOP_CFG_FPATH))
