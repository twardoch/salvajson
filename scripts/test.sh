#!/bin/bash
# this_file: scripts/test.sh
# Test script for salvajson

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
    log_info "Checking test dependencies..."
    
    cd "$PROJECT_ROOT"
    
    # Check if pytest is available
    if ! python3 -m pytest --version &> /dev/null; then
        log_error "pytest is not installed. Install with: pip install -e '.[test]'"
        exit 1
    fi
    
    # Check if pre-commit is available
    if ! command -v pre-commit &> /dev/null; then
        log_warning "pre-commit is not installed. Install with: pip install pre-commit"
    fi
    
    log_success "Test dependencies checked"
}

run_linting() {
    log_info "Running linting checks..."
    
    cd "$PROJECT_ROOT"
    
    # Run pre-commit hooks
    if command -v pre-commit &> /dev/null; then
        pre-commit run --all-files
    else
        log_warning "pre-commit not available, running individual tools..."
        
        # Run ruff
        if command -v ruff &> /dev/null; then
            ruff check src/ tests/
            ruff format --check src/ tests/
        else
            log_warning "ruff not available"
        fi
        
        # Run mypy
        if command -v mypy &> /dev/null; then
            mypy src/
        else
            log_warning "mypy not available"
        fi
    fi
    
    log_success "Linting checks completed"
}

run_tests() {
    log_info "Running test suite..."
    
    cd "$PROJECT_ROOT"
    
    # Run pytest with coverage
    python3 -m pytest \
        --verbose \
        --cov=src \
        --cov-report=term-missing \
        --cov-report=html:htmlcov \
        --cov-report=xml:coverage.xml \
        --junit-xml=test-results.xml \
        tests/
    
    log_success "Test suite completed"
}

run_smoke_tests() {
    log_info "Running smoke tests..."
    
    cd "$PROJECT_ROOT"
    
    # Test CLI functionality
    echo '{"test": "value"}' | python3 -m salvajson /dev/stdin > /dev/null
    
    # Test import
    python3 -c "import salvajson; print(f'Version: {salvajson.__version__}')"
    
    # Test basic functionality
    python3 -c "
import salvajson
result = salvajson.loads('{name: \"test\"}')
assert result == {'name': 'test'}
print('Basic functionality test passed')
"
    
    log_success "Smoke tests completed"
}

run_security_checks() {
    log_info "Running security checks..."
    
    cd "$PROJECT_ROOT"
    
    # Run bandit if available
    if command -v bandit &> /dev/null; then
        bandit -r src/ -f json -o bandit-report.json || true
        bandit -r src/
    else
        log_warning "bandit not available"
    fi
    
    # Check for known vulnerabilities in dependencies
    if command -v safety &> /dev/null; then
        safety check --json --output safety-report.json || true
        safety check
    else
        log_warning "safety not available"
    fi
    
    log_success "Security checks completed"
}

show_coverage_report() {
    log_info "Coverage report:"
    
    cd "$PROJECT_ROOT"
    
    if [ -f "coverage.xml" ]; then
        python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('coverage.xml')
root = tree.getroot()
coverage = root.attrib.get('line-rate', '0')
print(f'Line coverage: {float(coverage)*100:.1f}%')
"
    fi
    
    if [ -d "htmlcov" ]; then
        log_info "HTML coverage report available at: htmlcov/index.html"
    fi
}

show_help() {
    cat << EOF
Usage: $0 [OPTIONS]

Test script for salvajson

Options:
    -h, --help          Show this help message
    -f, --fast          Run tests without coverage
    -l, --lint-only     Run only linting checks
    -t, --test-only     Run only pytest tests
    -s, --smoke-only    Run only smoke tests
    --security          Run security checks
    --no-coverage       Skip coverage reporting
    --parallel          Run tests in parallel
    --verbose           Verbose output

Examples:
    $0                  # Run all tests
    $0 --fast           # Run tests without coverage
    $0 --lint-only      # Run only linting
    $0 --test-only      # Run only pytest
    $0 --smoke-only     # Run only smoke tests
    $0 --security       # Include security checks
EOF
}

# Parse command line arguments
FAST=false
LINT_ONLY=false
TEST_ONLY=false
SMOKE_ONLY=false
SECURITY=false
NO_COVERAGE=false
PARALLEL=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -f|--fast)
            FAST=true
            shift
            ;;
        -l|--lint-only)
            LINT_ONLY=true
            shift
            ;;
        -t|--test-only)
            TEST_ONLY=true
            shift
            ;;
        -s|--smoke-only)
            SMOKE_ONLY=true
            shift
            ;;
        --security)
            SECURITY=true
            shift
            ;;
        --no-coverage)
            NO_COVERAGE=true
            shift
            ;;
        --parallel)
            PARALLEL=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Main test process
main() {
    log_info "Starting test process..."
    
    check_dependencies
    
    if [ "$LINT_ONLY" = true ]; then
        run_linting
    elif [ "$TEST_ONLY" = true ]; then
        run_tests
        if [ "$NO_COVERAGE" = false ]; then
            show_coverage_report
        fi
    elif [ "$SMOKE_ONLY" = true ]; then
        run_smoke_tests
    else
        # Run all tests
        run_linting
        run_tests
        run_smoke_tests
        
        if [ "$SECURITY" = true ]; then
            run_security_checks
        fi
        
        if [ "$NO_COVERAGE" = false ]; then
            show_coverage_report
        fi
    fi
    
    log_success "Test process completed successfully!"
}

# Run main function
main "$@"