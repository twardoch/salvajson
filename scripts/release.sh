#!/bin/bash
# this_file: scripts/release.sh
# Release script for salvajson

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
    log_info "Checking release dependencies..."
    
    # Check git
    if ! command -v git &> /dev/null; then
        log_error "git is required but not installed"
        exit 1
    fi
    
    # Check if we're in a git repository
    if ! git rev-parse --git-dir &> /dev/null; then
        log_error "Not in a git repository"
        exit 1
    fi
    
    # Check semantic-release
    if ! command -v semantic-release &> /dev/null; then
        log_error "semantic-release is required but not installed"
        log_info "Install with: pip install python-semantic-release"
        exit 1
    fi
    
    log_success "Release dependencies checked"
}

check_git_status() {
    log_info "Checking git repository status..."
    
    cd "$PROJECT_ROOT"
    
    # Check if we're on main branch
    current_branch=$(git rev-parse --abbrev-ref HEAD)
    if [ "$current_branch" != "main" ]; then
        log_warning "Not on main branch (current: $current_branch)"
        if [ "$FORCE" = false ]; then
            log_error "Use --force to release from non-main branch"
            exit 1
        fi
    fi
    
    # Check if working directory is clean
    if ! git diff-index --quiet HEAD --; then
        log_error "Working directory is not clean. Commit or stash changes first."
        git status --porcelain
        exit 1
    fi
    
    # Check if we're up to date with remote
    if git remote | grep -q origin; then
        git fetch origin
        local_commit=$(git rev-parse HEAD)
        remote_commit=$(git rev-parse origin/main 2>/dev/null || echo "")
        
        if [ -n "$remote_commit" ] && [ "$local_commit" != "$remote_commit" ]; then
            log_warning "Local branch is not up to date with remote"
            if [ "$FORCE" = false ]; then
                log_error "Use --force to release anyway, or pull latest changes"
                exit 1
            fi
        fi
    fi
    
    log_success "Git repository status checked"
}

run_full_test_suite() {
    log_info "Running full test suite..."
    
    cd "$PROJECT_ROOT"
    
    # Run the test script
    if [ -f "$SCRIPT_DIR/test.sh" ]; then
        bash "$SCRIPT_DIR/test.sh" --security
    else
        log_warning "Test script not found, running basic tests..."
        python3 -m pytest
    fi
    
    log_success "Full test suite completed"
}

build_release() {
    log_info "Building release..."
    
    cd "$PROJECT_ROOT"
    
    # Clean previous builds
    rm -rf dist/ build/
    
    # Run the build script
    if [ -f "$SCRIPT_DIR/build.sh" ]; then
        bash "$SCRIPT_DIR/build.sh" --clean --verify
    else
        log_warning "Build script not found, running basic build..."
        python3 -m build
    fi
    
    log_success "Release build completed"
}

determine_version_bump() {
    log_info "Determining version bump..."
    
    cd "$PROJECT_ROOT"
    
    # Get current version
    current_version=$(python3 -c "import src.salvajson; print(src.salvajson.__version__)" 2>/dev/null || echo "0.0.0")
    log_info "Current version: $current_version"
    
    # Use semantic-release to determine next version
    next_version=$(semantic-release version --print 2>/dev/null || echo "")
    
    if [ -n "$next_version" ]; then
        log_info "Next version would be: $next_version"
    else
        log_info "No version bump needed based on commit history"
    fi
    
    echo "$next_version"
}

create_release() {
    log_info "Creating release..."
    
    cd "$PROJECT_ROOT"
    
    if [ "$DRY_RUN" = true ]; then
        log_info "DRY RUN: Would create release with semantic-release"
        semantic-release version --print
        return
    fi
    
    # Create release with semantic-release
    semantic-release publish
    
    log_success "Release created successfully"
}

show_release_info() {
    log_info "Release information:"
    
    cd "$PROJECT_ROOT"
    
    # Show latest tag
    latest_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "No tags found")
    log_info "Latest tag: $latest_tag"
    
    # Show recent commits
    log_info "Recent commits:"
    git log --oneline -5
    
    # Show build artifacts
    if [ -d "dist" ]; then
        log_info "Build artifacts:"
        ls -la dist/
    fi
}

show_help() {
    cat << EOF
Usage: $0 [OPTIONS]

Release script for salvajson

Options:
    -h, --help          Show this help message
    -d, --dry-run       Show what would be done without making changes
    -f, --force         Force release even with warnings
    --skip-tests        Skip running tests before release
    --skip-build        Skip building before release
    --major             Force major version bump
    --minor             Force minor version bump
    --patch             Force patch version bump
    --pre-release       Create pre-release version

Examples:
    $0                  # Standard release process
    $0 --dry-run        # Show what would be released
    $0 --force          # Force release from non-main branch
    $0 --skip-tests     # Skip tests (not recommended)
    $0 --patch          # Force patch version bump
EOF
}

# Parse command line arguments
DRY_RUN=false
FORCE=false
SKIP_TESTS=false
SKIP_BUILD=false
VERSION_BUMP=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --skip-build)
            SKIP_BUILD=true
            shift
            ;;
        --major)
            VERSION_BUMP="major"
            shift
            ;;
        --minor)
            VERSION_BUMP="minor"
            shift
            ;;
        --patch)
            VERSION_BUMP="patch"
            shift
            ;;
        --pre-release)
            VERSION_BUMP="prerelease"
            shift
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Main release process
main() {
    log_info "Starting release process..."
    
    check_dependencies
    check_git_status
    
    if [ "$SKIP_TESTS" = false ]; then
        run_full_test_suite
    fi
    
    if [ "$SKIP_BUILD" = false ]; then
        build_release
    fi
    
    next_version=$(determine_version_bump)
    
    if [ -z "$next_version" ] && [ "$FORCE" = false ]; then
        log_warning "No version bump needed based on commit history"
        log_info "Use --force to create a release anyway"
        exit 0
    fi
    
    create_release
    show_release_info
    
    log_success "Release process completed successfully!"
    
    if [ "$DRY_RUN" = false ]; then
        log_info "Don't forget to:"
        log_info "  1. Push the new tag: git push origin --tags"
        log_info "  2. Check the GitHub Actions workflow"
        log_info "  3. Verify the PyPI upload"
    fi
}

# Run main function
main "$@"