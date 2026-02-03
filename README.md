# uv-mermaid-cli

A CLI tool to convert Mermaid diagrams to images using Playwright.

## Installation

```bash
# Install with uv
uv tool install uv-mermaid-cli

# Install Playwright's Chromium browser
playwright install chromium
```

Or run directly without installing:

```bash
uvx uv-mermaid-cli render "graph TD; A-->B;" -o diagram.png
```

## Usage

### Basic Usage

```bash
# Render inline diagram
mermaid-cli render "graph TD; A[Start] --> B[End];" -o flow.png

# Render from file
mermaid-cli render -i diagram.mmd -o output.png

# Pipe from stdin
echo "graph TD; A-->B;" | mermaid-cli render -o flow.png
cat diagram.mmd | mermaid-cli render -o output.png
```

### Output Formats

```bash
# PNG (default)
mermaid-cli render "graph TD; A-->B;" -o diagram.png

# SVG
mermaid-cli render "graph TD; A-->B;" -o diagram.svg
```

### Themes

Available themes: `default`, `dark`, `forest`, `neutral`

```bash
mermaid-cli render "graph TD; A-->B;" -o diagram.png -t dark
mermaid-cli themes  # List all themes
```

### Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--output` | `-o` | `diagram.png` | Output file path |
| `--input` | `-i` | - | Input file path |
| `--format` | `-f` | auto | Output format (png/svg) |
| `--theme` | `-t` | `default` | Mermaid theme |
| `--background` | `-b` | `white` | Background color |
| `--width` | `-w` | `800` | Viewport width (px) |
| `--scale` | `-s` | `2.0` | Scale factor for resolution |
| `--quiet` | `-q` | - | Suppress output |

### Examples

```bash
# High resolution output
mermaid-cli render "sequenceDiagram; Alice->>Bob: Hello" -o seq.png -s 3

# Dark theme with transparent background
mermaid-cli render "pie title Pets; \"Dogs\": 50; \"Cats\": 30" -o pets.svg -t dark -b transparent

# Wide diagram
mermaid-cli render -i architecture.mmd -o arch.png -w 1200
```

## Supported Diagram Types

All Mermaid diagram types are supported:

- Flowcharts
- Sequence diagrams
- Class diagrams
- State diagrams
- Entity Relationship diagrams
- Gantt charts
- Pie charts
- And more...

See [Mermaid documentation](https://mermaid.js.org/intro/) for syntax.

## Development

```bash
# Clone the repo
git clone https://github.com/jhiggins-tech/uv-mermaid-cli
cd uv-mermaid-cli

# Install in development mode
uv sync --dev

# Run tests
uv run pytest

# Run the CLI
uv run mermaid-cli --help
```

## License

MIT
