# Security policy

## Reporting a problem

Please report a security problem privately, not in a public issue. Use GitHub's
private vulnerability reporting: on the repository, open Security, then
Report a vulnerability.

Include what you found, where, and how to reproduce it. You can expect a first
reply within a week.

## Scope

This repository holds Markdown, CSV, and static web files, plus a small Python
build. It holds no secrets and runs no server. Things worth reporting:

- a script, workflow, or page that could run untrusted input
- a leaked secret, token, or private term in any file or in the history
- a dependency or GitHub Actions workflow with a known vulnerability

Content corrections (wrong clause numbers, typos) are not security issues. Open
a normal issue or pull request for those.
