"""A simple command-line tool for dinglebop."""

import pprint

import click

from dinglebop.param_inference_maps import rebuild_all_maps
from dinglebop.collection_cfg import rebuild_collection_cfg_files
from dinglebop.shared import _dinglebop_cfg


@click.group(help="Utility dinglebop operations.")
def util():
    """Utility dinglebop operations."""
    pass


@util.command(help="Rebuild parameter inference maps.")
def rebuildmaps():
    """Rebuild parameter inference maps."""
    rebuild_all_maps()


@util.command(help="Rebuild collection attributes.")
def rebuildattr():
    """Rebuild collection attributes."""
    rebuild_collection_cfg_files()


@util.command(help="Print dinglebop's current configuration.")
def printcfg():
    """Print dinglebop's current configuration."""
    pprint.pprint(_dinglebop_cfg(), indent=1, width=10)
