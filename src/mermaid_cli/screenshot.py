"""Screenshot capture using Playwright."""

import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


class ScreenshotError(Exception):
    """Error during screenshot capture."""
    pass


class BrowserNotFoundError(ScreenshotError):
    """Raised when Chromium browser is not installed."""
    pass


def is_chromium_installed() -> bool:
    """Check if Playwright's Chromium browser is installed."""
    try:
        with sync_playwright() as p:
            # Try to get the executable path - this will fail if not installed
            browser = p.chromium.launch(headless=True)
            browser.close()
            return True
    except Exception as e:
        if "Executable doesn't exist" in str(e) or "browserType.launch" in str(e):
            return False
        # Some other error - assume it's installed but broken
        return True


def install_chromium(quiet: bool = False) -> bool:
    """Install Playwright's Chromium browser.

    Args:
        quiet: Suppress output if True

    Returns:
        True if installation succeeded, False otherwise
    """
    try:
        cmd = [sys.executable, "-m", "playwright", "install", "chromium"]
        if quiet:
            subprocess.run(cmd, check=True, capture_output=True)
        else:
            subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def capture_diagram(
    html_path: Path,
    output_path: Path,
    width: int = 800,
    scale: float = 2.0,
    output_format: str = "png",
    timeout: int = 10000,
) -> None:
    """Capture a screenshot of the rendered Mermaid diagram.

    Args:
        html_path: Path to the HTML file containing the diagram
        output_path: Path where the output image will be saved
        width: Viewport width in pixels
        scale: Device scale factor for higher resolution
        output_format: Output format ('png' or 'svg')
        timeout: Maximum time to wait for rendering in milliseconds

    Raises:
        ScreenshotError: If capture fails
    """
    try:
        with sync_playwright() as p:
            # Launch headless Chromium
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": width, "height": 600},
                device_scale_factor=scale,
            )
            page = context.new_page()

            # Navigate to the HTML file
            file_url = f"file://{html_path.absolute()}"
            page.goto(file_url, wait_until="networkidle")

            # Wait for Mermaid to finish rendering
            try:
                page.wait_for_selector(
                    'body[data-mermaid-ready="true"]',
                    timeout=timeout,
                )
            except PlaywrightTimeout:
                # Check if there's a parse error
                error_elem = page.query_selector(".error-text, .error-icon")
                if error_elem:
                    error_text = error_elem.text_content()
                    raise ScreenshotError(f"Mermaid syntax error: {error_text}")
                raise ScreenshotError(
                    "Timed out waiting for Mermaid to render. "
                    "Check your diagram syntax."
                )

            # Find the rendered diagram container
            container = page.query_selector("#container")
            if not container:
                raise ScreenshotError("Could not find rendered diagram container")

            if output_format == "svg":
                # Extract SVG content
                svg_element = container.query_selector("svg")
                if not svg_element:
                    raise ScreenshotError("Could not find SVG element in rendered diagram")

                # Get the outer HTML of the SVG
                svg_content = svg_element.evaluate("el => el.outerHTML")

                # Write SVG to file
                output_path.write_text(svg_content, encoding="utf-8")
            else:
                # Take PNG screenshot of the container
                container.screenshot(
                    path=str(output_path),
                    type="png",
                )

            browser.close()

    except PlaywrightTimeout as e:
        raise ScreenshotError(f"Playwright timeout: {e}")
    except Exception as e:
        if isinstance(e, ScreenshotError):
            raise
        # Check for common Playwright installation issues
        if "Executable doesn't exist" in str(e) or "browserType.launch" in str(e):
            raise BrowserNotFoundError("Chromium browser not found")
        raise ScreenshotError(f"Screenshot failed: {e}")
