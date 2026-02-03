"""HTML renderer for Mermaid diagrams."""

import tempfile
from pathlib import Path

# Mermaid CDN URL - using a stable version
MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background-color: {background};
            display: flex;
            justify-content: center;
            align-items: flex-start;
        }}
        #container {{
            display: inline-block;
        }}
        .mermaid {{
            font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', sans-serif;
        }}
    </style>
</head>
<body>
    <div id="container">
        <pre class="mermaid">
{diagram}
        </pre>
    </div>
    <script type="module">
        import mermaid from '{cdn}';
        mermaid.initialize({{
            startOnLoad: true,
            theme: '{theme}',
            securityLevel: 'loose',
        }});

        // Signal when rendering is complete
        mermaid.run().then(() => {{
            document.body.setAttribute('data-mermaid-ready', 'true');
        }});
    </script>
</body>
</html>
"""


def generate_html(
    diagram: str,
    theme: str = "default",
    background: str = "white",
) -> str:
    """Generate HTML content with embedded Mermaid diagram.

    Args:
        diagram: Mermaid diagram syntax
        theme: Mermaid theme (default, dark, forest, neutral)
        background: CSS background color

    Returns:
        Complete HTML string
    """
    # Escape HTML special characters in diagram
    diagram_escaped = (
        diagram
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    return HTML_TEMPLATE.format(
        diagram=diagram_escaped,
        theme=theme,
        background=background,
        cdn=MERMAID_CDN,
    )


def create_temp_html(
    diagram: str,
    theme: str = "default",
    background: str = "white",
) -> Path:
    """Create a temporary HTML file with the Mermaid diagram.

    Args:
        diagram: Mermaid diagram syntax
        theme: Mermaid theme
        background: CSS background color

    Returns:
        Path to the temporary HTML file
    """
    html_content = generate_html(diagram, theme, background)

    # Create temp file that persists until explicitly deleted
    fd, path = tempfile.mkstemp(suffix=".html", prefix="mermaid_")
    with open(fd, "w", encoding="utf-8") as f:
        f.write(html_content)

    return Path(path)
