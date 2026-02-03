"""Tests for the screenshot module."""

import pytest
from pathlib import Path

from mermaid_cli.screenshot import ScreenshotError


def test_screenshot_error_message():
    """Test ScreenshotError has correct message."""
    error = ScreenshotError("test error")
    assert str(error) == "test error"


# Note: Full screenshot tests require playwright with chromium installed.
# These are integration tests that should be run manually or in CI with
# playwright properly configured.
#
# Example integration test (requires playwright install chromium):
#
# def test_capture_diagram_png(tmp_path):
#     from mermaid_cli.renderer import create_temp_html
#     from mermaid_cli.screenshot import capture_diagram
#
#     html_path = create_temp_html("graph TD; A-->B;")
#     output_path = tmp_path / "test.png"
#
#     try:
#         capture_diagram(html_path, output_path)
#         assert output_path.exists()
#         assert output_path.stat().st_size > 0
#     finally:
#         html_path.unlink(missing_ok=True)
