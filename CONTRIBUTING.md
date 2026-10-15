# Contributing

Thank you for helping. Small, focused changes are easiest to review.

## Before you start

- Open an issue first for anything bigger than a typo, so we agree on the change.
- Do not copy text from ISO, COBIT, or other standards. Cite clause numbers and titles
  only, and paraphrase everything else.
- Write in American English (license, organization, color).

## Making a change

1. Fork the repository and branch from `main`. Name the branch `type/<issue number>-short-name`,
   for example `fix/12-typo-in-guide`.
2. Edit the sources, not the generated output. Files under `dist/` and most of `site/docs/`
   are built; change `methods/`, `sam-toolkit/`, `lifecycle/`, `practicum/`, or `build/` and run:

   ```
   make test
   make build
   ```

3. Commit the regenerated `dist/` and `site/` files together with your change. CI fails if they differ.
4. Use a conventional commit title, 50 characters or fewer: `type(scope): summary`
   (for example `fix(crosswalk): correct XW-014 clause`). On squash merge the pull request title is used,
   and `release-please` reads it to set the next version.
5. Open a pull request and fill in the template. A maintainer reviews every pull request.

## Crosswalk changes

Each row in `methods/crosswalk/crosswalk.csv` needs a `verified` date and at least one framework cell.
Record the evidence in `methods/crosswalk/sources.md`.

## Licensing

By contributing you agree your work is released under the MIT license in `LICENSE`.
Please follow `CODE_OF_CONDUCT.md`.
