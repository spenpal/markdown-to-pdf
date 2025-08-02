# Markdown to PDF

An opinionated, zero-configuration Docker container for converting Markdown to beautiful PDFs using Pandoc with optimized settings.

- **Zero configuration** - Just works out of the box
- **Optimized defaults** - Community-tested settings for best output
- **Lightning fast** - Uses Tectonic engine for quick compilation
- **Beautiful output** - Eisvogel template with professional typography
- **Simple usage** - One command, one file

## Features

- **PDF Engine**: Tectonic (fastest, self-contained)
- **Template**: Eisvogel (professional, technical documentation)
- **Typography**: DejaVu font family (excellent Unicode support)
- **Layout**: A4 paper with 2cm margins (international standard)
- **Highlighting**: Tango syntax highlighting for code blocks
- **Structure**: Auto table of contents, numbered sections

## Quick Start

### 1. Build the container

```bash
git clone https://github.com/spenpal/markdown-to-pdf.git
cd markdown-to-pdf
docker build -t md2pdf .
```

### 2. Convert your markdown

```bash
docker run --rm -v $(pwd):/data md2pdf document.md
```

That's it! Your `document.pdf` will be created in the same directory.

## Requirements

- Docker installed on your system
- Markdown files to convert

## License

MIT License - see [LICENSE](LICENSE) file for details.
