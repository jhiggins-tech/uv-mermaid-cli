"""Tests for the CLI module."""

import pytest
from click.testing import CliRunner

from mermaid_cli.cli import main, THEMES


@pytest.fixture
def runner():
    return CliRunner()


def test_version(runner):
    """Test version command."""
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "mermaid-cli" in result.output


def test_themes_command(runner):
    """Test themes command."""
    result = runner.invoke(main, ["themes"])
    assert result.exit_code == 0
    for theme in THEMES:
        assert theme in result.output


def test_render_no_input(runner):
    """Test render command with no input."""
    result = runner.invoke(main, ["render"])
    assert result.exit_code != 0
    # Either "No diagram provided" or "Empty diagram provided" depending on stdin state
    assert "diagram provided" in result.output or "Empty" in result.output


def test_render_empty_input(runner):
    """Test render command with empty input."""
    result = runner.invoke(main, ["render", ""])
    assert result.exit_code != 0


def test_render_with_stdin(runner):
    """Test render command with stdin input."""
    # This test will fail without playwright installed
    # It's here to verify the CLI argument parsing works
    result = runner.invoke(
        main,
        ["render", "-o", "test.png"],
        input="graph TD; A-->B;",
    )
    # Will fail due to playwright not being installed in test env
    # but should get past the argument parsing
    assert "No diagram provided" not in result.output
