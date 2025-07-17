# Development Guide

This document provides detailed instructions for developing, testing, and releasing salvajson.

## Quick Start

```bash
# Set up development environment
./dev.sh setup

# Run tests
./dev.sh test

# Build the project
./dev.sh build --clean

# Create a release (dry run)
./dev.sh release --dry-run
```

## Development Environment Setup

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- npm
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/twardoch/salvajson.git
   cd salvajson
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -e ".[dev,test]"
   cd js_src && npm ci && cd ..
   ```

4. **Set up pre-commit hooks:**
   ```bash
   pre-commit install
   pre-commit install --hook-type commit-msg
   ```

## Development Scripts

We provide several convenience scripts for common development tasks:

### Main Development Script

The `dev.sh` script provides a unified interface for all development tasks:

```bash
./dev.sh <command> [options]
```

**Available commands:**
- `setup` - Set up development environment
- `build` - Build the project
- `test` - Run tests
- `release` - Create a release
- `clean` - Clean build artifacts
- `lint` - Run linting only
- `coverage` - Show coverage report
- `version` - Show current version

### Individual Scripts

Located in the `scripts/` directory:

- `scripts/build.sh` - Build script
- `scripts/test.sh` - Test script
- `scripts/release.sh` - Release script

## Testing

### Running Tests

```bash
# Run all tests
./dev.sh test

# Run tests without coverage
./dev.sh test --fast

# Run only linting
./dev.sh test --lint-only

# Run only pytest
./dev.sh test --test-only

# Run only smoke tests
./dev.sh test --smoke-only

# Include security checks
./dev.sh test --security
```

### Test Structure

```
tests/
├── test_salvajson.py    # Main test suite
├── data/                # Test data files
└── conftest.py         # Test configuration
```

### Coverage

Tests maintain >80% coverage. View coverage reports:

```bash
# Generate coverage report
./dev.sh test

# View HTML coverage report
./dev.sh coverage
```

## Building

### Local Build

```bash
# Standard build
./dev.sh build

# Clean build
./dev.sh build --clean

# Build with verification
./dev.sh build --verify

# Skip dependency installation
./dev.sh build --skip-deps
```

### Binary Build

Build standalone executables:

```bash
# Install PyInstaller
pip install pyinstaller

# Build binary
pyinstaller salvajson.spec

# Test binary
echo '{"test": "value"}' | ./dist/salvajson
```

## Release Process

### Semantic Versioning

The project uses semantic versioning with git tags:

- **v1.0.0** - Major release
- **v1.1.0** - Minor release
- **v1.1.1** - Patch release

### Creating a Release

1. **Ensure clean state:**
   ```bash
   git status
   git pull origin main
   ```

2. **Run full test suite:**
   ```bash
   ./dev.sh test --security
   ```

3. **Preview release:**
   ```bash
   ./dev.sh release --dry-run
   ```

4. **Create release:**
   ```bash
   ./dev.sh release
   ```

5. **Push tag (if not auto-pushed):**
   ```bash
   git push origin --tags
   ```

### Release Automation

The release process is automated using:

- **python-semantic-release** - Determines version bumps based on conventional commits
- **GitHub Actions** - CI/CD pipeline for testing and publishing
- **PyPI** - Package distribution

## Git Workflow

### Conventional Commits

We use [Conventional Commits](https://www.conventionalcommits.org/) for automated versioning:

```bash
feat: add new feature (minor bump)
fix: fix a bug (patch bump)
docs: update documentation (patch bump)
style: code formatting (patch bump)
refactor: code refactoring (patch bump)
test: add tests (patch bump)
chore: maintenance tasks (patch bump)

feat!: breaking change (major bump)
fix!: breaking bug fix (major bump)
```

### Branch Strategy

- **main** - Production-ready code
- **feature/** - Feature branches
- **hotfix/** - Critical bug fixes
- **release/** - Release preparation

## Code Quality

### Linting and Formatting

```bash
# Run all checks
./dev.sh lint

# Individual tools
ruff check src/ tests/
ruff format src/ tests/
mypy src/
```

### Pre-commit Hooks

Automatically run on every commit:

- **Ruff** - Python linting and formatting
- **Mypy** - Type checking
- **Prettier** - JS/JSON/MD formatting
- **Bandit** - Security scanning
- **Commitlint** - Commit message validation

### Security

```bash
# Run security checks
bandit -r src/
safety check

# Include in test suite
./dev.sh test --security
```

## CI/CD

### GitHub Actions

Located in `.github/workflows/`:

- **ci.yml** - Main CI/CD pipeline
- **update-js.yml** - JS dependency updates

### Pipeline Stages

1. **Prepare** - Build package and artifacts
2. **Test** - Run tests on multiple platforms/Python versions
3. **Security** - Security scanning
4. **Build Binaries** - Create standalone executables
5. **Publish** - Upload to PyPI (on tags)
6. **Release** - Create GitHub release (on tags)

### Multiplatform Testing

Tests run on:
- **Operating Systems:** Ubuntu, Windows, macOS
- **Python Versions:** 3.10, 3.11, 3.12

## Architecture

### Project Structure

```
salvajson/
├── src/salvajson/          # Main package
│   ├── __init__.py         # Package exports
│   ├── salvajson.py        # Core functionality
│   ├── salvajson.js        # Bundled JavaScript
│   └── __main__.py         # CLI entry point
├── js_src/                 # JavaScript source
│   ├── salvajson.src.js    # Main JS file
│   └── build.esbuild.js    # Build configuration
├── tests/                  # Test suite
├── scripts/                # Development scripts
└── .github/workflows/      # CI/CD workflows
```

### Key Components

- **Python-JavaScript Bridge** - PythonMonkey for JS interop
- **JSON Repair** - jsonic library for lenient parsing
- **High Performance** - orjson for fast JSON operations
- **Build System** - Hatch for modern Python packaging
- **Version Management** - hatch-vcs + semantic-release

## Troubleshooting

### Common Issues

1. **JavaScript build fails:**
   ```bash
   cd js_src && npm ci && npm run build
   ```

2. **Version not updating:**
   ```bash
   git fetch --tags
   pip install -e ".[dev,test]"
   ```

3. **Tests failing:**
   ```bash
   ./dev.sh clean
   ./dev.sh test --fast
   ```

4. **Pre-commit hooks failing:**
   ```bash
   pre-commit run --all-files
   ```

### Getting Help

- Check the [README.md](README.md) for basic usage
- Look at the [GitHub Issues](https://github.com/twardoch/salvajson/issues)
- Review the [test suite](tests/) for examples

## Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Run tests:** `./dev.sh test`
5. **Submit a pull request**

All contributions must:
- Pass all tests
- Follow code style guidelines
- Include appropriate tests
- Use conventional commit messages