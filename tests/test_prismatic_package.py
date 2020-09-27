import pytest
from click.testing import CliRunner

from prismatic_package import main


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_base_cli(runner: CliRunner) -> None:
    """Test that empty cli is working"""
    result = runner.invoke(main.cli)
    assert result.exit_code == 0


def test_echo_succeeds_from_group(runner: CliRunner) -> None:
    """Make sure we can call echo from the cli group"""
    result = runner.invoke(main.cli, "echo")
    assert result.exit_code == 0


def test_echo_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(main.echo)
    assert result.exit_code == 0


def test_get_my_ip(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(main.what_is_my_ip)
    assert result.exit_code == 0
