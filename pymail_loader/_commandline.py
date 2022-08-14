import typing
from email.policy import Policy

import typer

from pymail_loader import version

app = typer.Typer(name="pymail_loader")


POLICY_FACTORY: typing.Dict[typing.Literal["default", "strict", "smtp", "smtputf8", "http"], Policy]


def unpack_recipients(ctx: typer.Context, recipients: typing.List[str]) -> typing.Optional[typing.List[str]]:
    """
    Validates the mail `--to` input, for any of the inputs, if they are a valid
    file on disk (csv) we will extract the email addresses from the file delimiting
    on `,`.  The emails are then squashed into a flat list and handed off to the
    `Email` instance.
    """
    if not ctx.resilient_parsing:
        return recipients
    return None


def validate_policy(ctx: typer.Context):
    ...


def validate_provider(ctx: typer.Context):
    ...


@app.command(name="bulk")
def send(
    from_addr: str = typer.Option(..., "--from", "-f"),
    to_addrs: typing.List[str] = typer.Option(..., "--to", "-t", callback=unpack_recipients),
    cc: typing.List[str] = typer.Option(None, "--cc", callback=unpack_recipients),
    bcc: typing.List[str] = typer.Option(None, "--bcc", callback=unpack_recipients),
    policy: str = typer.Option("default", case_sensitive=False, callback=validate_policy),
    subject: str = typer.Option("", "--subject", "-sub", "-s"),
    message: str = typer.Option("", "--message", "-msg", "-m"),
    html: str = typer.Option("", "--html"),
    charset: str = typer.Option(None, "--charset", "-cs"),
    headers: typing.List[str] = typer.Option(None, "--headers", "-h"),
    verbosity: int = typer.Option(0, "-v", count=True),
    host: str = typer.Option("localhost", "--smtp"),
    port: int = typer.Option(25, "--port", "-p"),
    tls: bool = typer.Option(False, "--tls"),
    provider: str = typer.Option(None, "--provider", callback=validate_provider),
    copies: int = typer.Option(1, "--copies"),
    directory: str = typer.Option(None, "--eml-dir"),
    envelope_sender: str = typer.Option(None, "--envelope-sender", "-es"),
    envelope_recipients: typing.List[str] = typer.Option(..., "--envelope-recipients", "-er"),
):
    """
    The entry point of pymail_loader.
    :param from_addr: The from address on the email header (also used implicitly as the envelope sender)
    :param to_addrs: The sender addresses (multiple) on the email header (also used as the envelope recipient)
    :param cc:
    :param bcc:
    :param policy:
    :param subject:
    :param message:
    :param html:
    :param charset:
    :param headers:
    :param verbosity:
    :param host:
    :param port:
    :param tls:
    :param provider:
    :param copies:
    :param directory:
    :param envelope_sender:
    :param envelope_recipients:
    :return:
    """
    typer.secho(f"pymail_loader loaded.. (verbosity: {verbosity})", fg=typer.colors.BRIGHT_GREEN, bold=True)


def version_callback(value: bool):
    if value:
        typer.secho(f"pymail_loader version: {version}", fg=typer.colors.BRIGHT_GREEN, bold=True)
        raise typer.Exit()


@app.callback()
def main(version: bool = typer.Option(None, "--version", callback=version_callback, is_eager=True)):
    """
    A powerful python email command line tool.
    """
    if version:
        typer.secho(f"pymail_loader: {version}", fg=typer.colors.BRIGHT_GREEN, bold=True)
        raise typer.Exit()
