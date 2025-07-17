# Release Checklist

This checklist ensures a smooth and complete release process for salvajson.

## Pre-Release Preparation

### 1. Code Quality
- [ ] All tests pass locally: `./dev.sh test`
- [ ] Code coverage is ≥80%
- [ ] Security checks pass: `./dev.sh test --security`
- [ ] Linting passes: `./dev.sh lint`
- [ ] Documentation is up-to-date

### 2. Version Management
- [ ] Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)
- [ ] `CHANGELOG.md` is updated (or will be auto-generated)
- [ ] Version bump is appropriate (major/minor/patch)

### 3. Dependencies
- [ ] All dependencies are up-to-date
- [ ] JavaScript dependencies are current: `cd js_src && npm audit`
- [ ] Python dependencies have no known vulnerabilities: `safety check`

### 4. Testing
- [ ] All tests pass on multiple Python versions (3.10, 3.11, 3.12)
- [ ] JavaScript build works: `cd js_src && npm run build`
- [ ] CLI functionality works: `echo '{"test": "value"}' | python -m salvajson`
- [ ] Package import works: `python -c "import salvajson; print(salvajson.__version__)"`

## Release Process

### 1. Environment Check
- [ ] On `main` branch: `git branch --show-current`
- [ ] Working directory is clean: `git status`
- [ ] Up-to-date with remote: `git pull origin main`

### 2. Build and Test
- [ ] Clean build succeeds: `./dev.sh build --clean --verify`
- [ ] Full test suite passes: `./dev.sh test --security`
- [ ] Binary builds work locally (optional): `pyinstaller salvajson.spec`

### 3. Release Dry Run
- [ ] Preview release: `./dev.sh release --dry-run`
- [ ] Version bump looks correct
- [ ] Release notes are appropriate

### 4. Create Release
- [ ] Create release: `./dev.sh release`
- [ ] Git tag is created: `git tag -l`
- [ ] Release commit is pushed: `git log --oneline -5`

### 5. GitHub Actions
- [ ] CI/CD pipeline starts: Check GitHub Actions
- [ ] All jobs pass (prepare, test, security, build-binaries)
- [ ] PyPI publication succeeds
- [ ] GitHub release is created with assets

## Post-Release Verification

### 1. Package Availability
- [ ] Package is available on PyPI: `pip install salvajson==<version>`
- [ ] GitHub release has all assets (wheel, tar.gz, binaries)
- [ ] Release notes are accurate

### 2. Installation Testing
- [ ] Install from PyPI in fresh environment: `pip install salvajson`
- [ ] Basic functionality works: `python -c "import salvajson; print(salvajson.__version__)"`
- [ ] CLI works: `python -m salvajson --help`

### 3. Binary Testing
- [ ] Download Linux binary from GitHub release
- [ ] Download Windows binary from GitHub release
- [ ] Download macOS binary from GitHub release
- [ ] Test basic functionality: `./salvajson-linux-x64 input.json`

### 4. Documentation
- [ ] README.md reflects current version
- [ ] CHANGELOG.md is updated
- [ ] GitHub release notes are comprehensive
- [ ] PyPI page shows correct information

## Rollback Procedure

If issues are discovered after release:

### 1. Immediate Actions
- [ ] Identify the issue and scope
- [ ] Communicate to users (GitHub issue/discussion)
- [ ] Consider if hotfix is needed

### 2. Hotfix Process
- [ ] Create hotfix branch: `git checkout -b hotfix/v<version>`
- [ ] Apply minimal fix
- [ ] Test thoroughly
- [ ] Create hotfix release: `./dev.sh release --patch`

### 3. Yanking (if necessary)
- [ ] Yank problematic version from PyPI: `pip install twine && twine upload --yank <version>`
- [ ] Update GitHub release to mark as pre-release
- [ ] Communicate the issue and resolution

## Automation Status

### Currently Automated
- ✅ Version determination (semantic-release)
- ✅ Changelog generation (semantic-release)
- ✅ Git tagging (semantic-release)
- ✅ Multi-platform testing (GitHub Actions)
- ✅ Security scanning (GitHub Actions)
- ✅ Binary builds (GitHub Actions)
- ✅ PyPI publishing (GitHub Actions)
- ✅ GitHub release creation (GitHub Actions)

### Manual Steps
- 🔄 Release initiation (`./dev.sh release`)
- 🔄 Pre-release testing and verification
- 🔄 Post-release verification
- 🔄 Issue response and hotfixes

## Version History

Track major releases and their characteristics:

| Version | Date | Type | Notes |
|---------|------|------|-------|
| v1.0.0  | TBD  | Major | Initial stable release |

## Emergency Contacts

- **Primary Maintainer**: Adam Twardoch (@twardoch)
- **Backup**: [Add backup maintainer]
- **PyPI Admin**: [Add PyPI admin contact]

## Release Schedule

- **Regular releases**: As needed based on feature completion
- **Security releases**: ASAP for critical vulnerabilities
- **Maintenance releases**: Monthly for dependency updates

## Metrics to Track

After each release, track:
- [ ] Download numbers (PyPI, GitHub)
- [ ] Issue reports
- [ ] Performance metrics
- [ ] User feedback

---

**Note**: This checklist should be updated as the release process evolves. Keep it current with any changes to automation or procedures.