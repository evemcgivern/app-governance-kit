# Style guide

This guide is public and MIT licensed, like the rest of the repo. It is written for human contributors and for AI agents. It records what `site/style.css` and the pages in `site/` do today. It does not propose a redesign. When the guide and a page disagree, flag it in the PR.

Read it before you create or change a page, copy, CSS, or a page template in `build/agk/`. A new contributor can read it in about ten minutes.

## Contents

1. [Design tokens](#design-tokens)
2. [Components](#components)
3. [Page patterns](#page-patterns)
4. [Accessibility rules](#accessibility-rules)
5. [Writing rules](#writing-rules)
6. [Keeping this guide current](#keeping-this-guide-current)

## Design tokens

All tokens live in the `:root` block at the top of `site/style.css`. The dark theme repeats them twice: once under `@media (prefers-color-scheme: dark)` for `:root:not([data-theme="light"])`, and once for `:root[data-theme="dark"]` (the theme switch). Use `var(--name)`. Do not write a hex value in a page or a component rule.

### Palette

| Token | Light | Dark | Use |
| --- | --- | --- | --- |
| `--bg` | `#f6f7f9` | `#10151b` | Page background |
| `--surface` | `#ffffff` | `#1a212b` | Cards, header, panels |
| `--fg` | `#1a212b` | `#e7ebef` | Body text |
| `--muted` | `#4d5762` | `#a7b1bb` | Secondary text, meta lines |
| `--border` | `#dde1e6` | `#2c3641` | Hairlines, dividers |
| `--accent` | `#1f4c5e` | `#7fc2dd` | Links, primary buttons, current page |
| `--accent-fg` | `#ffffff` | `#0c1720` | Text on `--accent` |
| `--focus` | `#1f4c5e` | `#9fd4e8` | Focus ring color |
| `--code-bg` | `#eef1f4` | `#131a22` | Code and prompt blocks |
| `--chip-bg` | `#eef3f5` | `#1e2a33` | Chips, zebra rows, hover fill |
| `--control-border` | `#767f89` | `#6b7886` | Form control borders |
| `--glow` | `rgba(31, 76, 94, 0.10)` | `rgba(127, 194, 221, 0.10)` | Soft light at the top of the page |

### Nav group tokens

Each of the four nav groups has a label color, a wash (the group background) and a hover fill. Values are light / dark.

| Group | Label | Wash | Hover |
| --- | --- | --- | --- |
| Start | `--nav-start` `#14596f` / `#7fc2dd` | `--nav-start-wash` `#dcedf3` / `#17323d` | `--nav-start-hover` `#c4e0ea` / `#1f4453` |
| Do | `--nav-do` `#8a4b00` / `#f0b765` | `--nav-do-wash` `#fbeccf` / `#35280f` | `--nav-do-hover` `#f6dca8` / `#46351a` |
| Learn | `--nav-learn` `#4a3fa8` / `#b8aef5` | `--nav-learn-wash` `#e6e3f8` / `#272347` | `--nav-learn-hover` `#d3cef2` / `#342f5c` |
| Explore | `--nav-explore` `#a3224f` / `#f19ab6` | `--nav-explore-wash` `#f9e1e8` / `#3b1f2a` | `--nav-explore-hover` `#f2cbd7` / `#4d2837` |

Group colors belong to the header nav. Do not use them as page decoration.

### Shadows and motion

| Token | Value (light) | Use |
| --- | --- | --- |
| `--shadow` | 1px ring plus two soft layers | Cards, panels, buttons at rest |
| `--shadow-hover` | Stronger ring and a wider layer | Button hover |
| `--ease` | `cubic-bezier(0.2, 0, 0, 1)` | All transitions |

Transitions run 0.15s to 0.2s on `background-color`, `color`, `box-shadow`, `filter` and `scale`. Pressed controls use `scale: 0.96`.

### Type scale

The font stack is the system stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`. Body line height is 1.6.

| Role | Size |
| --- | --- |
| Page `h1` (`.hero h1`) | `clamp(1.9rem, 5vw, 2.9rem)`, line height 1.1 |
| Doc page `h1` | `clamp(1.7rem, 4.5vw, 2.4rem)`, line height 1.15 |
| Lede (`.hero p.positioning`) | 1.1rem, `--muted` |
| Card title (`.case-card h3`) | 1.05rem |
| Body | 1rem |
| Meta (`.meta`) | 0.92rem, `--muted` |
| Breadcrumb, pill links | 0.85rem |
| Nav group label | 0.7rem, uppercase, 0.06em spacing |

Headings use `text-wrap: balance`. Paragraphs and list items use `text-wrap: pretty` and cap at `46rem`.

### Spacing, width and radii

| Item | Value |
| --- | --- |
| Page width (`main`, header inner) | `max-width: 68rem`, side padding `1.25rem` |
| Page padding (`main`) | `2rem 1.25rem 4rem` |
| Gap between sections | `2.5rem` (`main section + section`) |
| Reading width | `46rem`; `.prose-wide` is `55rem` |
| Card grid | `repeat(auto-fit, minmax(15rem, 1fr))`, gap `1.25rem` |
| Card padding | `1.25rem` |
| Layout breakpoint | `46rem` (the wheel and nav switch to wide layouts here) |

| Radius | Use |
| --- | --- |
| `999px` | Pills: buttons, nav links, chips, action links |
| `12px` | Cards and panels |
| `0.4rem` | Result boxes, chips inside panels |
| `0.25rem` | Skip link |

### Focus ring

One rule covers every control: `:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }`. Do not remove or replace it. Do not use `outline: none` without an equal replacement.

## Components

Each snippet is copied from the real markup. Use the component when its description matches.

### Header and grouped nav

Use on every top-level page. The markup is the same on all of them (a test checks that). Groups are Start, Do, Learn and Explore. Each link has a tooltip with an id the link points to. `aria-current="page"` marks the current page.

```html
<div class="nav-group">
  <p class="nav-group__label" id="nav-group-explore">Explore</p>
  <ul aria-labelledby="nav-group-explore">
    <li><a href="lifecycle.html" aria-current="page" aria-describedby="tip-lifecycle">Application lifecycle</a><span class="nav-tip" role="tooltip" id="tip-lifecycle">...</span></li>
  </ul>
</div>
```

Do not add classes or inline styles to nav markup. CSS picks each group by its label id.

### Breadcrumb

Use on every page except the home page. The last item is plain text with `aria-current`.

```html
<nav class="breadcrumb" aria-label="Breadcrumb">
  <ol>
    <li><a href="index.html">Home</a></li>
    <li><span aria-current="page">Case studies</span></li>
  </ol>
</nav>
```

### H1 and lede

One `h1` per page, inside `.hero`, followed by one lede paragraph.

```html
<section class="hero">
  <h1>Questions to ask at each stage</h1>
  <p class="positioning">An application moves through six stages from request to retirement. ...</p>
</section>
```

### Section heading

Every section is a `<section>` named by its `h2` with `aria-labelledby`. Headings nest one level at a time: `h1`, `h2`, `h3`.

```html
<section aria-labelledby="cases-heading">
  <h2 id="cases-heading">The six cases</h2>
  ...
</section>
```

### Card and card grid

Use a card for one item. Use the grid for two or more cards side by side. The tools page uses one card per tool.

```html
<article class="card" id="hardware-lifecycle">
  <h2>Hardware lifecycle check</h2>
  <p class="meta">hardware-lifecycle (devices, from purchase to wipe).</p>
  <p>Check a device fleet for hardware overdue for refresh ...</p>
</article>
```

### Case card (card variant)

Use on hub pages that list items: a title link, a one-sentence summary, then up to two meta lines (what it is, where it fits). The list is a `ul` so a screen reader announces the count.

```html
<ul class="case-list card-grid">
  <li class="card case-card">
    <h3><a href="impact-map.html">Themes by stage</a></h3>
    <p class="case-card__summary">Every crosswalk theme against the six stages.</p>
    <p class="meta case-card__tool">Kind: grid</p>
    <p class="meta case-card__step">Fits: all six stages</p>
  </li>
</ul>
```

When a meta line has a link, add visually hidden text so the link still makes sense out of context: `playbook step 3<span class="visually-hidden">: Week 1, stop the bleeding</span>`.

### Tool facts card (card variant)

Use on a page that compares several tools or items on the same fields. Each card has a title link to the item's detail card, an optional `Limit:` meta line, and a definition list with the same labels in the same order on every card. At 46rem and wider each row is a label column and a text column; below that, the label sits above its text, so the cards stack at 390 px. The fields on `tools.html` are What it does, You give it, You get, Use it when and Decision stays with. Write "Not found." where the source does not say.

```html
<ul class="tool-overview case-list card-grid">
  <li class="card tool-card">
    <h3><a href="#access-review">Access review pack</a></h3>
    <dl class="tool-facts">
      <div><dt>What it does</dt><dd>Matches every account to a person ...</dd></div>
      <div><dt>Decision stays with</dt><dd>The application owner decides each removal.</dd></div>
    </dl>
  </li>
</ul>
```

`tests/test_tools_overview.py` checks one card per method, the five fields, and that each title link reaches a real card.

### Link list

Use for a short run of links, often under a card.

```html
<ul class="link-list">
  <li><a href="docs/hardware-lifecycle/method.html">Method<span class="visually-hidden"> for Hardware lifecycle check</span></a></li>
</ul>
```

### Details disclosure

Use to fold long explanation below the main content. Put the `details` inside a `section.read-notes` with its own `h2`. The summary names what is inside.

```html
<section class="read-notes" aria-labelledby="loop-heading">
  <h2 id="loop-heading">How the stages fit together</h2>
  <details>
    <summary>The council, the gates and the loop</summary>
    <p class="lc-together">...</p>
  </details>
</section>
```

### Tag, badge and chip

- `.nav-badge`: a small filled pill inside a nav link (uppercase, 0.7rem).
- `.step-chip`: a pill on `--chip-bg` that names a playbook step on doc pages.
- `.lc-rule-xw`: an outlined pill that names a crosswalk row in the wheel panel.

Use a chip for a short label, never for a sentence. Do not make a chip the only way to learn something.

### Buttons and action links

```html
<a class="button" href="...">Primary action</a>
<a class="button button--ghost" href="impact-map.html">See themes by stage</a>
<p class="visual-actions">
  <a class="visual-actions__link" href="downloads/lifecycle-wheel.svg">Download this diagram (SVG)</a>
</p>
```

Use `.button` for the one main action in a block, `.button--ghost` for a second action, and `.visual-actions__link` for download and print links next to a diagram or table. Buttons are at least 44 px tall. Action links are at least 40 px tall.

### Tables

Wrap every wide table in a named, focusable scroll region. The first column is a row header.

```html
<div class="table-scroll" tabindex="0" role="region" aria-label="Cross-certification task matrix, scroll sideways to see more">
  <table>...</table>
</div>
```

### Practicum checker blocks

Each exercise has a step line, files, a hand-in area, and a result region. The result region is always in the page, empty until a check runs, with `role="status"` and `aria-live="polite"`. Never hide it.

```html
<p class="pr-step">Practice for playbook step 2.</p>
<div class="pr-result" id="pr-result-program-setup" role="status" aria-live="polite"></div>
```

After a check, focus moves to the result heading. Pass and fail change the border color and also say so in text.

### Doc pages with download actions

Generated from Markdown by `build/agk/docs.py`. Do not hand-edit them. The page has a breadcrumb, a back link, an `h1`, download and print actions, a jump list, then `.doc-body`.

```html
<div class="visual-actions doc-actions">
  <a class="visual-actions__link" href="questions.docx">Download Word (.docx)</a>
  <button type="button" class="visual-actions__link doc-print doc-secondary" onclick="window.print()">Print or save as PDF</button>
</div>
```

## Page patterns

Parts appear in this order. Skip a part only if the page has no use for it.

**Landing page (`index.html`)**

1. Header and nav
2. Hero: `h1`, lede, main buttons
3. Hero graphic or wheel with its caption
4. Sections that each end in one call to action
5. Footer

**Hub page with cards (`case-studies.html`, `lifecycle.html`)**

1. Header and nav, then breadcrumb
2. Hero: `h1` and one lede
3. The thing the reader came to use (wheel, stage chooser or card list)
4. Related items as case cards: title link, summary, kind or tool, where it fits
5. Long explanation in a `details` section below
6. Footer

**Case or exercise page**

1. Header, breadcrumb, `h1`, lede
2. The list of cases or exercises
3. Per case: a step line, a one-paragraph answer, then the situation, what the records showed, what the tool did, the decisions that stayed with people, what a real team would still check, and how to prove the benefit
4. Mark each human decision with **Decision needed:**

**Doc page (generated)**

1. Header, breadcrumb to the parent page
2. Back link and print button
3. `h1`, download actions, reading time
4. Jump list, then the body
5. Previous and next links where the doc is a playbook step

## Accessibility rules

Tests pin these rules. A change that breaks one fails `make test`.

| Rule | Where it is pinned |
| --- | --- |
| Nav group text meets 4.5:1 on every wash and hover tint, in light, system dark and switch dark | `tests/test_nav_color.py` |
| Group rails meet 3:1 against the header | `tests/test_nav_color.py` |
| Each group defines label, wash and hover tokens; both dark blocks match | `tests/test_nav_color.py` |
| Nav markup has no color classes or inline styles | `tests/test_nav_color.py` |
| Scroll wrappers are named, focusable regions; the first column is a row header | `tests/test_a11y_mobile.py` |
| Practicum result regions are `role="status"` and never hidden; focus moves to the result heading | `tests/test_a11y_mobile.py` |
| Nav and step links are 44 px tall at phone widths; inputs use 1rem text | `tests/test_a11y_mobile.py` |
| View links name their page; a failed copy shows a visible note | `tests/test_a11y_mobile.py` |
| Nav, breadcrumb, titles, descriptions and `aria-current` are consistent on every page | `tests/test_site_pages.py` |
| Hub card lists are labelled, summaries are present, links resolve | `tests/test_case_studies_page.py`, `tests/test_lifecycle_page.py` |
| The tools overview has one card per method, five fields each, and links to real cards | `tests/test_tools_overview.py` |

Rules that live in CSS and no test pins. Check them by eye:

- Focus ring: keep the 3px `:focus-visible` rule. Check every new control in light and dark.
- Reduced motion: keep the `prefers-reduced-motion: reduce` block that shortens animation and transitions.
- Target size: make every link or button at least 24 px tall. The site uses 40 px for pills and 44 px for buttons.
- Link text: write link text that makes sense out of context. Do not write "click here" or a bare "Method". Add visually hidden text when the visible label is short.
- Color: do not use color alone to show state. Pair it with words.
- Layout: check each page at 390 px, with no sideways page scroll, in light and dark.

## Writing rules

Follow these on every page, card, label and alt text that readers see.

- Write to the reader as "you".
- Use plain words. Say "use", not "utilize".
- Use American English: license, organization, color, program.
- Use contractions where they sound natural.
- Do not write stock quips or filler openers.
- Use a comma, colon or period where it does the job. Do not lean on em dashes.
- Paraphrase framework material. Never reproduce text from ISO, COBIT, IAITAM or other standards or courseware. Cite clause numbers and titles only. The scan fails on quoted runs of 15 or more words.
- Use only the fictional Halden Logistics data in `demo-estate/` for examples. Never use real company, client or person data.
- Write "Not found." where a figure is missing. Do not estimate.
- Describe limits and unverified items plainly. Say what the source was and that nobody checked it.
- Mark each point where a person decides with **Decision needed:**.
- Leave employer names and role titles out of public text.

## Keeping this guide current

- When you add or change a token, component or pattern, update this guide in the same PR.
- `tests/test_style_guide.py` reads the `:root` block of `site/style.css` and fails if a palette or nav token is missing here.
- If a page departs from this guide, say so in the PR. Do not diverge silently.
