import click

from . import __version__


@click.group()
def cli() -> None:
    """Main CLI entrypoint used to regroup all commands"""
    pass


@cli.command()
@click.version_option(version=__version__)
def echo() -> None:
    """Return a simple Hello World message"""
    click.echo("Hello, world!")


@cli.command()
@click.version_option(version=__version__)
def what_is_my_ip() -> None:
    """Display information about your ip in color

    Requires to install with the prismatic-package[my_ip] optional requirements
    """
    import requests
    from pjson import core  # type: ignore
    from pygments.lexers import JsonLexer  # type: ignore

    res = requests.get("https://ifconfig.co/json")
    code = core.format_code(res.content)
    text = core.color_yo_shit(code, JsonLexer())
    click.echo(text)
