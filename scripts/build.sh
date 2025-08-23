#!/bin/bash
# this_file: scripts/build.sh
# Build script for salvajson

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DIST_DIR="$PROJECT_ROOT/dist"
BUILD_DIR="$PROJECT_ROOT/build"

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

check_dependencies() {
    log_info "Checking dependencies..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is required but not installed"
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        log_error "Node.js is required but not installed"
        exit 1
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        log_error "npm is required but not installed"
        exit 1
    fi
    
    log_success "All dependencies are available"
}

clean_build() {
    log_info "Cleaning previous build artifacts..."
    
    # Remove dist and build directories
    rm -rf "$DIST_DIR" "$BUILD_DIR"
    
    # Clean Python cache
    find "$PROJECT_ROOT" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "$PROJECT_ROOT" -type f -name "*.pyc" -delete 2>/dev/null || true
    
    log_success "Build artifacts cleaned"
}

install_dependencies() {
    log_info "Installing Python dependencies..."
    
    cd "$PROJECT_ROOT"
    
    # Install development dependencies
    python3 -m pip install --upgrade pip
    python3 -m pip install -e ".[dev,test]"
    
    log_info "Installing JavaScript dependencies..."
    
    # Install JS dependencies
    cd "$PROJECT_ROOT/js_src"
    npm ci
    
    log_success "Dependencies installed"
}

build_javascript() {
    log_info "Building JavaScript bundle..."
    
    cd "$PROJECT_ROOT/js_src"
    npm run build
    
    log_success "JavaScript bundle built"
}

build_python() {
    log_info "Building Python package..."
    
    cd "$PROJECT_ROOT"
    python3 -m build
    
    log_success "Python package built"
}

verify_build() {
    log_info "Verifying build artifacts..."
    
    # Check if dist directory exists and has files
    if [ ! -d "$DIST_DIR" ]; then
        log_error "Distribution directory not found"
        exit 1
    fi
    
    # Check for wheel file
    if ! ls "$DIST_DIR"/*.whl 1> /dev/null 2>&1; then
        log_error "No wheel file found in dist directory"
        exit 1
    fi
    
    # Check for source distribution
    if ! ls "$DIST_DIR"/*.tar.gz 1> /dev/null 2>&1; then
        log_error "No source distribution found in dist directory"
        exit 1
    fi
    
    log_success "Build artifacts verified"
    log_info "Build contents:"
    ls -la "$DIST_DIR"
}

show_help() {
    cat << EOF
Usage: $0 [OPTIONS]

Build script for salvajson

Options:
    -h, --help      Show this help message
    -c, --clean     Clean build artifacts before building
    -v, --verify    Verify build artifacts after building
    --skip-deps     Skip dependency installation
    --skip-js       Skip JavaScript build
    --skip-python   Skip Python build

Examples:
    $0                  # Standard build
    $0 --clean          # Clean build
    $0 --verify         # Build and verify
    $0 --skip-deps      # Build without installing dependencies
EOF
}

# Parse command line arguments
CLEAN=false
VERIFY=false
SKIP_DEPS=false
SKIP_JS=false
SKIP_PYTHON=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -c|--clean)
            CLEAN=true
            shift
            ;;
        -v|--verify)
            VERIFY=true
            shift
            ;;
        --skip-deps)
            SKIP_DEPS=true
            shift
            ;;
        --skip-js)
            SKIP_JS=true
            shift
            ;;
        --skip-python)
            SKIP_PYTHON=true
            shift
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Main build process
main() {
    log_info "Starting build process..."
    
    check_dependencies
    
    if [ "$CLEAN" = true ]; then
        clean_build
    fi
    
    if [ "$SKIP_DEPS" = false ]; then
        install_dependencies
    fi
    
    if [ "$SKIP_JS" = false ]; then
        build_javascript
    fi
    
    if [ "$SKIP_PYTHON" = false ]; then
        build_python
    fi
    
    if [ "$VERIFY" = true ]; then
        verify_build
    fi
    
    log_success "Build completed successfully!"
}

# Run main function
main "$@"