# Product Requirements Document: uv-mermaid-cli

## Overview

A Python CLI tool that converts Mermaid diagram syntax into image files. The tool uses Playwright for headless browser rendering of Mermaid diagrams via the official Mermaid.js CDN, then captures screenshots to produce output images.

## Problem Statement

Developers and technical writers often need to generate diagram images from Mermaid syntax for use in documentation, presentations, or other contexts where live rendering isn't available. Existing solutions either require Node.js tooling or external services. This tool provides a Python-native solution managed via `uv`.

## Goals

1. **Simple CLI interface** - Accept Mermaid syntax and output image files with minimal configuration
2. **Headless operation** - Run without visible browser windows for automation/CI use
3. **High-quality output** - Produce crisp PNG/SVG images suitable for documentation
4. **Easy installation** - Installable via `uv` with a single command
5. **Cross-platform** - Works on Linux, macOS, and Windows

## Non-Goals (v1)

- GUI interface
- Live preview/watch mode
- Standalone `.exe` distribution (future consideration)
- PDF output format
- Batch processing of multiple files (CLI handles one at a time; scripting can batch)

## Technical Architecture

### Components

```
┌─────────────────────────────────────────────────────────┐
│                     CLI Layer (Click)                   │
│  - Argument parsing                                     │
│  - Input validation                                     │
│  - Output path handling                                 │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   Renderer Module                       │
│  - Generate temporary HTML with Mermaid CDN            │
│  - Configure diagram theme/styling                     │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              Screenshot Module (Playwright)             │
│  - Launch headless Chromium                            │
│  - Navigate to HTML                                    │
│  - Wait for Mermaid render                             │
│  - Capture element screenshot                          │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                     Output Handler                      │
│  - Save PNG/SVG to specified path                      │
│  - Handle overwrite prompts                            │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Package Manager | uv | Fast, modern Python package manager |
| CLI Framework | Click | Mature, well-documented, easy to use |
| Browser Automation | Playwright | Reliable, supports headless mode, good API |
| Mermaid Rendering | Mermaid.js via CDN | Official library, always up-to-date |
| Build System | Hatchling | Modern, PEP 517 compliant |

### Project Structure

```
uv-mermaid-cli/
├── pyproject.toml          # Project metadata and dependencies
├── README.md               # Usage documentation
├── PRD.md                  # This document
├── src/
│   └── mermaid_cli/
│       ├── __init__.py     # Package init with version
│       ├── cli.py          # Click CLI definition
│       ├── renderer.py     # HTML generation for Mermaid
│       └── screenshot.py   # Playwright screenshot logic
└── tests/
    ├── __init__.py
    ├── test_cli.py
    ├── test_renderer.py
    └── test_screenshot.py
```

## Functional Requirements

### FR1: Input Methods

The CLI must accept Mermaid syntax via:

1. **String argument**: Direct syntax on command line
   ```bash
   mermaid-cli render "graph TD; A-->B;" -o diagram.png
   ```

2. **File input**: Path to a `.mmd` or `.mermaid` file
   ```bash
   mermaid-cli render -i diagram.mmd -o diagram.png
   ```

3. **Stdin**: Piped input
   ```bash
   echo "graph TD; A-->B;" | mermaid-cli render -o diagram.png
   ```

### FR2: Output Formats

| Format | Extension | Method |
|--------|-----------|--------|
| PNG | `.png` | Playwright screenshot |
| SVG | `.svg` | Extract rendered SVG from DOM |

### FR3: Configuration Options

| Option | Flag | Default | Description |
|--------|------|---------|-------------|
| Output path | `-o, --output` | `diagram.png` | Output file path |
| Input file | `-i, --input` | None | Input file path |
| Format | `-f, --format` | Auto from extension | `png` or `svg` |
| Theme | `-t, --theme` | `default` | Mermaid theme (default, dark, forest, neutral) |
| Background | `-b, --background` | `white` | Background color (CSS color or `transparent`) |
| Width | `-w, --width` | `800` | Viewport width in pixels |
| Scale | `-s, --scale` | `2` | Screenshot scale factor for higher DPI |
| Quiet | `-q, --quiet` | `false` | Suppress non-error output |

### FR4: Commands

| Command | Description |
|---------|-------------|
| `render` | Render Mermaid syntax to image (main command) |
| `version` | Display version information |
| `themes` | List available Mermaid themes |

### FR5: Error Handling

- Invalid Mermaid syntax: Display Mermaid.js parse error message
- Missing input: Clear error with usage hint
- Output path issues: Check write permissions before rendering
- Playwright failures: Helpful message suggesting `playwright install`

## Non-Functional Requirements

### NFR1: Performance

- Render a simple diagram in < 3 seconds on typical hardware
- Browser instance reuse for potential future batch mode

### NFR2: Installation

```bash
# Install the tool
uv tool install uv-mermaid-cli

# Or run directly without install
uvx uv-mermaid-cli render "graph TD; A-->B;" -o diagram.png
```

Post-install, user must run `playwright install chromium` (documented in README).

### NFR3: Dependencies

Core runtime dependencies:
- `click>=8.0`
- `playwright>=1.40`

Development dependencies:
- `pytest>=7.0`
- `pytest-asyncio` (if using async Playwright API)

## User Stories

### US1: Quick Diagram Generation
> As a developer, I want to quickly convert a Mermaid diagram string to a PNG so I can paste it into documentation.

### US2: File-Based Workflow
> As a technical writer, I want to maintain `.mmd` source files and regenerate images when diagrams change.

### US3: CI Integration
> As a DevOps engineer, I want to generate diagram images in CI pipelines for automated documentation builds.

### US4: Theme Customization
> As a designer, I want to generate diagrams with different themes to match my documentation's visual style.

## Example Usage

```bash
# Basic usage with inline diagram
mermaid-cli render "graph TD; A[Start] --> B[End];" -o flow.png

# From file with dark theme
mermaid-cli render -i architecture.mmd -o architecture.png -t dark

# High-resolution output
mermaid-cli render "sequenceDiagram; Alice->>Bob: Hello" -o seq.png -s 3

# SVG output with transparent background
mermaid-cli render "pie title Pets; \"Dogs\": 50; \"Cats\": 30" -o pets.svg -b transparent

# Piped input
cat diagram.mmd | mermaid-cli render -o output.png
```

## Success Criteria

1. Tool installs cleanly via `uv tool install`
2. All four input methods work correctly
3. PNG and SVG outputs render correctly
4. All Mermaid diagram types are supported (flowchart, sequence, class, etc.)
5. Themes apply correctly
6. Error messages are clear and actionable

## Open Questions

1. **Async vs Sync Playwright API?** - Sync API is simpler; async may be needed for future batch mode
2. **Bundle Chromium?** - Adds ~150MB; currently requiring separate `playwright install`
3. **Config file support?** - `.mermaidrc` for default options? (Defer to v2)

## Timeline Estimate

| Phase | Tasks |
|-------|-------|
| Phase 1 | Project setup, basic CLI, inline string rendering |
| Phase 2 | File input, stdin, output formats |
| Phase 3 | Themes, configuration options, error handling |
| Phase 4 | Tests, documentation, build/publish |

---

**Status**: Draft - Awaiting Alignment
**Author**: Claude
**Date**: 2025-02-03
