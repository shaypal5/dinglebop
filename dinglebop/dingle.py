"""Define dingles."""

from .exceptions import (
    ConfigurationException,
)
from .shared import (
    DINGLEBOP_CFG_FPATH,
)


# === Configuration exception messages ==

MISSING_IDX_CONF_MSG = (
    "Mandatory index information is missing from the configuration of the {} "
    "dingle in the {} configuration file. Please add the required information."
)


class Dingle(object):
    """An instance of the dinglebop dataset storage and versioning system.

    Arguments
    ---------
    name : str
        The name of this dingle.
    conf_dict : dict
        A configuration mapping for this dingle.
    """

    def __init__(self, name, conf_dict):
        try:
            idx_conf = conf_dict['index']
        except KeyError:
            raise ConfigurationException(
                MISSING_IDX_CONF_MSG.format(name, DINGLEBOP_CFG_FPATH))

