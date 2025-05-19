"""
Tests for the Athena CLI.
"""

from typer.testing import CliRunner

from athena.cli import app

runner = CliRunner()

def test_cli_help():
    """Test that the CLI help command works."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "AI knowledge management assistant" in result.output

def test_cli_init():
    """Test that the init command works."""
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert "Initializing Athena" in result.output

def test_cli_process():
    """Test that the process command works."""
    result = runner.invoke(app, ["process"])
    assert result.exit_code == 0
    assert "Processing notes" in result.output

def test_cli_connect():
    """Test that the connect command works."""
    result = runner.invoke(app, ["connect"])
    assert result.exit_code == 0
    assert "Analyzing connections" in result.output

def test_cli_recommend():
    """Test that the recommend command works."""
    result = runner.invoke(app, ["recommend"])
    assert result.exit_code == 0
    assert "Generating recommendations" in result.output 