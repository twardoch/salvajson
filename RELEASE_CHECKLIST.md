# Release Checklist

This checklist ensures a smooth and complete release process for **salvajson**.

---

## Pre-Release Preparation

### 1. Code Quality
- [ ] All tests pass locally: `./dev.sh test`
- [ ] Code coverage ≥80%
- [ ] Security checks pass: `./dev.sh test --security`
- [ ] Linting passes: `./dev.sh lint`
- [ ] Documentation is current

### 2. Version Management
- [ ] Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)
- [ ] `CHANGELOG.md` updated or will be auto-generated
- [ ] Version bump (major/minor/patch) is correct

### 3. Dependencies
- [ ] All dependencies are up-to-date
- [ ] JavaScript dependencies audited: `cd js_src && npm audit`
- [ ] Python dependencies secure: `safety check`

### 4. Testing
- [ ] Tests pass on Python 3.10, 3.11, 3.12
- [ ] JavaScript build works: `cd js_src && npm run build`
- [ ] CLI functions correctly: `echo '{"test": "value"}' | python -m salvajson`
- [ ] Package imports without error: `python -c "import salvajson; print(salvajson.__version__)"`

---

## Release Process

### 1. Environment Check
- [ ] On `main` branch: `git branch --show-current`
- [ ] Working directory clean: `git status`
- [ ] Local repo synced with remote: `git pull origin main`

### 2. Build and Test
- [ ] Clean build succeeds: `./dev.sh build --clean --verify`
- [ ] Full test suite passes: `./dev.sh test --security`
- [ ] Binary builds work locally (optional): `pyinstaller salvajson.spec`

### 3. Release Dry Run
- [ ] Preview release: `./dev.sh release --dry-run`
- [ ] Version bump looks accurate
- [ ] Release notes make sense

### 4. Create Release
- [ ] Run release command: `./dev.sh release`
- [ ] Git tag created: `git tag -l`
- [ ] Release commit pushed: `git log --oneline -5`

### 5. GitHub Actions
- [ ] CI/CD pipeline triggered (check GitHub Actions)
- [ ] All jobs pass (prepare, test, security, build-binaries)
- [ ] PyPI publication successful
- [ ] GitHub release created with assets

---

## Post-Release Verification

### 1. Package Availability
- [ ] Installable from PyPI: `pip install salvajson==<version>`
- [ ] GitHub release includes all assets (wheel, tar.gz, binaries)
- [ ] Release notes match changes

### 2. Installation Testing
- [ ] Install in fresh environment: `pip install salvajson`
- [ ] Import works: `python -c "import salvajson; print(salvajson.__version__)"`
- [ ] CLI responds: `python -m salvajson --help`

### 3. Binary Testing
- [ ] Download Linux binary from GitHub
- [ ] Download Windows binary from GitHub
- [ ] Download macOS binary from GitHub
- [ ] Basic functionality test: `./salvajson-linux-x64 input.json`

### 4. Documentation
- [ ] README.md shows correct version
- [ ] CHANGELOG.md is current
- [ ] GitHub release notes are complete
- [ ] PyPI page has correct metadata

---

## Rollback Procedure

If issues appear after release:

### 1. Immediate Actions
- [ ] Identify and scope the issue
- [ ] Notify users (GitHub issue or discussion)
- [ ] Decide if a hotfix is necessary

### 2. Hotfix Process
- [ ] Create hotfix branch: `git checkout -b hotfix/v<version>`
- [ ] Apply minimal fix
- [ ] Run full tests
- [ ] Release hotfix: `./dev.sh release --patch`

### 3. Yanking (if needed)
- [ ] Yank version from PyPI: `twine upload --yank <version>`
- [ ] Mark GitHub release as pre-release
- [ ] Announce resolution

---

## Automation Status

### Automated
- ✅ Version determination (via semantic-release)
- ✅ Changelog generation
- ✅ Git tagging
- ✅ Multi-platform testing
- ✅ Security scanning
- ✅ Binary builds
- ✅ PyPI publishing
- ✅ GitHub release creation

### Manual
- 🔄 Release initiation (`./dev.sh release`)
- 🔄 Pre-release verification
- 🔄 Post-release checks
- 🔄 Handling post-release issues

---

## Version History

| Version | Date | Type  | Notes                  |
|---------|------|-------|------------------------|
| v1.0.0  | TBD  | Major | Initial stable release |

---

## Emergency Contacts

- **Primary Maintainer**: Adam Twardoch (@twardoch)  
- **Backup**: [Add backup maintainer]  
- **PyPI Admin**: [Add PyPI admin contact]  

---

## Release Schedule

- **Regular releases**: On demand  
- **Security releases**: ASAP  
- **Maintenance releases**: Monthly  

---

## Metrics to Track

After each release:
- [ ] Download stats (PyPI, GitHub)
- [ ] New issues reported
- [ ] Performance data
- [ ] User feedback

---

**Note**: Update this checklist as release workflows change. Keep it aligned with automation and team practices.