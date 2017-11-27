"""Utility functions for dinglebop."""

import json

from .shared import DINGLEBOP_CFG_FPATH
from .dingle import Dingle
from .exceptions import ConfigurationException


MISSING_DINGLES_CONF_MSG = (
    "Mandatory dingle information is missing from the dinglebop configuration "
    "file at {}. Please add the required information."
)


def inject_dingle_attributes(module_obj):
    """Injects the given object with attributes per dingle configured.

    Arguments
    ---------
    module_obj : object
        The object to inject with Dingle objects as attributes.
    """
    with open(DINGLEBOP_CFG_FPATH, 'r') as cfg_file:
        cfg_dict = json.load(cfg_file)
        try:
            dingles = cfg_dict['dingles']
            for dingle_name in dingles:
                dingle_obj = Dingle(
                    name=dingle_name,
                    conf_dict=dingles[dingle_name],
                )
                setattr(module_obj, dingle_name, dingle_obj)
        except KeyError:
            raise ConfigurationException(MISSING_DINGLES_CONF_MSG)
