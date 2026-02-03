"""Tests for the renderer module."""

import os
from pathlib import Path

from mermaid_cli.renderer import generate_html, create_temp_html


def test_generate_html_basic():
    """Test basic HTML generation."""
    diagram = "graph TD; A-->B;"
    html = generate_html(diagram)

    assert "graph TD; A--&gt;B;" in html  # Escaped
    assert "mermaid" in html
    assert "theme: 'default'" in html


def test_generate_html_with_theme():
    """Test HTML generation with custom theme."""
    html = generate_html("graph TD; A-->B;", theme="dark")
    assert "theme: 'dark'" in html


def test_generate_html_with_background():
    """Test HTML generation with custom background."""
    html = generate_html("graph TD; A-->B;", background="transparent")
    assert "background-color: transparent" in html


def test_generate_html_escapes_special_chars():
    """Test that special characters are escaped."""
    diagram = "graph TD; A[<script>alert(1)</script>]-->B;"
    html = generate_html(diagram)

    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_create_temp_html():
    """Test temporary HTML file creation."""
    diagram = "graph TD; A-->B;"
    path = create_temp_html(diagram)

    try:
        assert path.exists()
        assert path.suffix == ".html"
        content = path.read_text()
        assert "mermaid" in content
    finally:
        path.unlink(missing_ok=True)
