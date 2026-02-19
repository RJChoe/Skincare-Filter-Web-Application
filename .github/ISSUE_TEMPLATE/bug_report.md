---
name: Bug Report
about: Report a bug for autonomous fixing
title: "[BUG] "
labels: bug
assignees: ''
---

## Description

<!-- Provide a clear and concise description of the bug -->

## Reproduction Steps

1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior

<!-- What should happen -->

## Actual Behavior

<!-- What actually happens -->

## Error Messages

```
Paste error traceback here
```

## Environment

- **Python Version:** 3.13 (from `.python-version`)
- **Django Version:** 6.0 (from `pyproject.toml`)
- **Browser:** [e.g., Chrome 120, Firefox 121, Safari 17] (if UI bug)
- **OS:** [e.g., Windows 11, macOS 14, Ubuntu 22.04]

## Relevant Code

- **File:** `path/to/file.py`
- **Line:** [line number or range]

## Tests

- [ ] Unit test reproducing bug attached (preferred)
- [ ] Integration test reproducing bug attached
- [ ] Manual reproduction steps only

## Additional Context

<!-- Add any other context about the problem here -->
<!-- Screenshots, logs, configuration files, etc. -->

---

**For AI Agents:**
- Read error logs and traceback carefully
- Check relevant code, tests, and configuration
- Diagnose root cause without asking for guidance
- Implement minimal fix with regression test
- Verify fix locally before committing
