#!/bin/bash
# this_file: dev.sh
# Developer convenience script for salvajson

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$SCRIPT_DIR/scripts"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_help() {
    cat << EOF
Usage: $0 <command> [options]

Developer convenience script for salvajson

Commands:
    build [options]         Build the project
    test [options]          Run tests
    release [options]       Create a release
    setup                   Set up development environment
    clean                   Clean build artifacts
    lint                    Run linting only
    coverage                Show coverage report
    version                 Show current version
    help                    Show this help message

Build options:
    --clean                 Clean before building
    --verify                Verify build artifacts
    --skip-deps             Skip dependency installation
    --skip-js               Skip JavaScript build
    --skip-python           Skip Python build

Test options:
    --fast                  Run tests without coverage
    --lint-only             Run only linting checks
    --test-only             Run only pytest tests
    --smoke-only            Run only smoke tests
    --security              Run security checks
    --no-coverage           Skip coverage reporting
    --parallel              Run tests in parallel

Release options:
    --dry-run               Show what would be done
    --force                 Force release even with warnings
    --skip-tests            Skip running tests before release
    --skip-build            Skip building before release
    --major                 Force major version bump
    --minor                 Force minor version bump
    --patch                 Force patch version bump

Examples:
    $0 setup                # Set up development environment
    $0 build --clean        # Clean build
    $0 test --fast          # Quick test run
    $0 release --dry-run    # Preview release
    $0 lint                 # Run linting only
    $0 coverage             # Show coverage report
EOF
}

setup_dev_environment() {
    log_info "Setting up development environment..."
    
    cd "$SCRIPT_DIR"
    
    # Install Python dependencies
    python3 -m pip install --upgrade pip
    python3 -m pip install -e ".[dev,test]"
    
    # Install JS dependencies
    cd js_src
    npm ci
    cd ..
    
    # Install pre-commit hooks
    pre-commit install
    pre-commit install --hook-type commit-msg
    
    log_success "Development environment set up successfully!"
}

clean_artifacts() {
    log_info "Cleaning build artifacts..."
    
    cd "$SCRIPT_DIR"
    
    # Remove build artifacts
    rm -rf dist/ build/ htmlcov/ .coverage coverage.xml test-results.xml
    rm -rf src/salvajson.egg-info/
    
    # Clean Python cache
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    
    # Clean JS artifacts
    rm -rf js_src/node_modules/.cache/
    
    log_success "Build artifacts cleaned"
}

show_version() {
    cd "$SCRIPT_DIR"
    
    # Try to get version from installed package
    if python3 -c "import salvajson; print(f'Installed version: {salvajson.__version__}')" 2>/dev/null; then
        :
    else
        log_warning "Package not installed in development mode"
    fi
    
    # Show git info
    if git rev-parse --git-dir &> /dev/null; then
        echo "Git branch: $(git rev-parse --abbrev-ref HEAD)"
        echo "Git commit: $(git rev-parse --short HEAD)"
        
        # Show latest tag
        latest_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "No tags")
        echo "Latest tag: $latest_tag"
    fi
}

show_coverage() {
    cd "$SCRIPT_DIR"
    
    if [ -f "coverage.xml" ]; then
        python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('coverage.xml')
root = tree.getroot()
coverage = root.attrib.get('line-rate', '0')
print(f'Line coverage: {float(coverage)*100:.1f}%')
"
    else
        log_warning "No coverage report found. Run tests first."
    fi
    
    if [ -d "htmlcov" ]; then
        log_info "HTML coverage report available at: htmlcov/index.html"
        
        # Try to open in browser on macOS/Linux
        if command -v xdg-open &> /dev/null; then
            xdg-open htmlcov/index.html
        elif command -v open &> /dev/null; then
            open htmlcov/index.html
        fi
    fi
}

run_lint() {
    cd "$SCRIPT_DIR"
    
    log_info "Running linting checks..."
    
    if command -v pre-commit &> /dev/null; then
        pre-commit run --all-files
    else
        log_warning "pre-commit not available, running individual tools..."
        
        # Run ruff
        if command -v ruff &> /dev/null; then
            ruff check src/ tests/
            ruff format --check src/ tests/
        fi
        
        # Run mypy
        if command -v mypy &> /dev/null; then
            mypy src/
        fi
    fi
    
    log_success "Linting completed"
}

# Main function
main() {
    if [ $# -eq 0 ]; then
        show_help
        exit 1
    fi
    
    command=$1
    shift
    
    case $command in
        build)
            if [ -f "$SCRIPTS_DIR/build.sh" ]; then
                bash "$SCRIPTS_DIR/build.sh" "$@"
            else
                log_error "Build script not found"
                exit 1
            fi
            ;;
        test)
            if [ -f "$SCRIPTS_DIR/test.sh" ]; then
                bash "$SCRIPTS_DIR/test.sh" "$@"
            else
                log_error "Test script not found"
                exit 1
            fi
            ;;
        release)
            if [ -f "$SCRIPTS_DIR/release.sh" ]; then
                bash "$SCRIPTS_DIR/release.sh" "$@"
            else
                log_error "Release script not found"
                exit 1
            fi
            ;;
        setup)
            setup_dev_environment
            ;;
        clean)
            clean_artifacts
            ;;
        lint)
            run_lint
            ;;
        coverage)
            show_coverage
            ;;
        version)
            show_version
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"