"""CLI interface for Mermaid diagram rendering."""

import sys
from pathlib import Path

import click

from . import __version__
from .renderer import create_temp_html
from .screenshot import capture_diagram, ScreenshotError


THEMES = ["default", "dark", "forest", "neutral"]


@click.group()
@click.version_option(version=__version__, prog_name="mermaid-cli")
def main():
    """Convert Mermaid diagrams to images."""
    pass


@main.command()
@click.argument("diagram", required=False)
@click.option(
    "-i", "--input",
    "input_file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Input file containing Mermaid diagram (.mmd or .mermaid)",
)
@click.option(
    "-o", "--output",
    type=click.Path(dir_okay=False, path_type=Path),
    default="diagram.png",
    help="Output file path (default: diagram.png)",
)
@click.option(
    "-f", "--format",
    "output_format",
    type=click.Choice(["png", "svg"]),
    default=None,
    help="Output format (default: inferred from output extension)",
)
@click.option(
    "-t", "--theme",
    type=click.Choice(THEMES),
    default="default",
    help="Mermaid theme (default: default)",
)
@click.option(
    "-b", "--background",
    default="white",
    help="Background color (CSS color or 'transparent', default: white)",
)
@click.option(
    "-w", "--width",
    type=int,
    default=800,
    help="Viewport width in pixels (default: 800)",
)
@click.option(
    "-s", "--scale",
    type=float,
    default=2.0,
    help="Scale factor for higher resolution (default: 2.0)",
)
@click.option(
    "-q", "--quiet",
    is_flag=True,
    help="Suppress non-error output",
)
def render(
    diagram: str | None,
    input_file: Path | None,
    output: Path,
    output_format: str | None,
    theme: str,
    background: str,
    width: int,
    scale: float,
    quiet: bool,
):
    """Render a Mermaid diagram to an image.

    DIAGRAM can be provided as a string argument, via --input file, or piped via stdin.

    Examples:

        mermaid-cli render "graph TD; A-->B;" -o flow.png

        mermaid-cli render -i diagram.mmd -o output.png

        echo "graph TD; A-->B;" | mermaid-cli render -o flow.png
    """
    # Determine input source
    if diagram:
        mermaid_content = diagram
    elif input_file:
        mermaid_content = input_file.read_text(encoding="utf-8")
    elif not sys.stdin.isatty():
        mermaid_content = sys.stdin.read()
    else:
        raise click.UsageError(
            "No diagram provided. Pass a diagram string, use --input, or pipe via stdin."
        )

    mermaid_content = mermaid_content.strip()
    if not mermaid_content:
        raise click.UsageError("Empty diagram provided.")

    # Determine output format from extension if not specified
    if output_format is None:
        ext = output.suffix.lower()
        if ext == ".svg":
            output_format = "svg"
        else:
            output_format = "png"

    # Ensure output has correct extension
    if output_format == "svg" and output.suffix.lower() != ".svg":
        output = output.with_suffix(".svg")
    elif output_format == "png" and output.suffix.lower() not in (".png", ""):
        output = output.with_suffix(".png")

    if not quiet:
        click.echo(f"Rendering diagram to {output}...")

    # Create temporary HTML
    html_path = create_temp_html(mermaid_content, theme, background)

    try:
        # Capture screenshot
        capture_diagram(
            html_path=html_path,
            output_path=output,
            width=width,
            scale=scale,
            output_format=output_format,
        )

        if not quiet:
            click.echo(f"Done! Output saved to {output}")

    except ScreenshotError as e:
        raise click.ClickException(str(e))
    finally:
        # Clean up temp file
        html_path.unlink(missing_ok=True)


@main.command()
def themes():
    """List available Mermaid themes."""
    click.echo("Available themes:")
    for theme in THEMES:
        click.echo(f"  - {theme}")


if __name__ == "__main__":
    main()
