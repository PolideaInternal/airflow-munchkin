# -*- coding: utf-8 -*-

"""Console script for airflow_munchkin."""
import sys
import click


@click.command()
def main(args=None):  # pylint: disable=unused-argument
    """Console script for airflow_munchkin."""
    click.echo(
        "Replace this message by putting your code into " "airflow_munchkin.cli.main"
    )
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
