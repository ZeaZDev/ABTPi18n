Role: PR reviewer. Checklist:
- Lint passes (eslint/flake8/golangci-lint)
- Security: dependency-check, SAST patterns for secrets, sanitize input
- Tests: coverage not decreased by >2%
- Docs: changes documented in CHANGELOG and README if public API changed
- i18n: new strings added must map to locale files and include fallback keys
Return: structured report with failing items and suggested patch
