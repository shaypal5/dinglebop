"""A command-line interface for dinglebop."""

import click

from .util_cli import util


@click.group(help="A command-line interface for dinglebop.")
def cli():
    """A command-line interface for dinglebop."""
    pass


cli.add_command(util)
