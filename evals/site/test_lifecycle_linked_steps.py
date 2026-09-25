"""Regression check for site/lifecycle.html's linked-step navigation (task 14h).

Covers: deep-linking to a #<stage>/<item-id> URL, following a linked-item
anchor (pushState + back-link + focus), returning via the in-panel back
link and via the real browser back button, and the "Show what this
affects" overlay (aria-pressed + legend + wheel dimming).

This is a standalone Playwright script, NOT wired into `make test`
(tests/ uses stdlib unittest and has zero third-party dependencies; this
script depends on the third-party `playwright` package plus its browser
binaries, which are not otherwise used anywhere in this repo). Written
because the task brief asked for a Playwright regression script for this
click-path; flagged in the QA report so a human can decide whether a new
third-party dependency belongs in this repo at all.

Setup:
    pip install playwright
    playwright install chromium

Run (a static file server must already be serving site/ — this script
does not start one for you):
    cd site && python3 -m http.server 8935 &
    python3 evals/site/test_lifecycle_linked_steps.py http://localhost:8935

Exits 0 if every check passes, 1 otherwise. Prints one PASS/FAIL line per
check rather than using a test framework's assert-and-stop, so a single
failure doesn't hide the results of the checks after it.
"""
import sys

from playwright.sync_api import sync_playwright

FAILURES = []


def check(label, condition, detail=""):
    if condition:
        print(f"PASS: {label}")
    else:
        print(f"FAIL: {label}" + (f" ({detail})" if detail else ""))
        FAILURES.append(label)


def main(base_url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # --- 1. Deep link opens directly with no back link -----------------
        page.goto(f"{base_url}/lifecycle.html#deploy/q-deploy-inventory")
        page.wait_for_timeout(200)
        active_id = page.evaluate("document.activeElement && document.activeElement.id")
        back_hidden = page.evaluate("document.getElementById('lc-back-link').hidden")
        check("deep link focuses the target item", active_id == "q-deploy-inventory", active_id)
        check("deep link shows no back link", back_hidden is True)

        # --- 2. Follow a 'blocks' linked-item anchor forward ----------------
        page.goto(f"{base_url}/lifecycle.html#deploy")
        page.wait_for_timeout(200)
        anchor = page.locator(".lc-link-anchor", has_text="Blocks: Operate").first
        anchor.click()
        page.wait_for_timeout(200)
        check("blocks link navigates to the target item",
              page.evaluate("location.hash") == "#operate/q-operate-access-review",
              page.evaluate("location.hash"))
        check("blocks link focuses the target item",
              page.evaluate("document.activeElement && document.activeElement.id") == "q-operate-access-review")
        back_text = page.evaluate("document.getElementById('lc-back-link').textContent")
        check("back link names the stage the link came from", "Deploy" in back_text, back_text)

        # --- 3. Real browser back button restores the origin, no back link -
        page.go_back()
        page.wait_for_timeout(200)
        check("browser back restores the origin hash", page.evaluate("location.hash") == "#deploy")
        check("browser back hides the back link",
              page.evaluate("document.getElementById('lc-back-link').hidden") is True)

        # --- 4. In-panel back link returns to the origin item --------------
        # The only "Blocks: Operate" anchor under Deploy belongs to the RULE
        # r-deploy-inventory (lifecycle/links.csv has no such link from the
        # question q-deploy-inventory), so the origin item is the rule.
        anchor2 = page.locator(".lc-link-anchor", has_text="Blocks: Operate").first
        anchor2.click()
        page.wait_for_timeout(200)
        page.locator("#lc-back-link a").click()
        page.wait_for_timeout(200)
        check("in-panel back link returns to the origin item",
              page.evaluate("location.hash") == "#deploy/r-deploy-inventory",
              page.evaluate("location.hash"))
        # Fixed 2026-09-25 (found in exploratory QA the same day): the back
        # link used to ping-pong instead of clearing — clicking it now
        # returns to the origin item as a true "back" step, with no new
        # back link shown.
        back_hidden_after_return = page.evaluate("document.getElementById('lc-back-link').hidden")
        check("back link clears after being used (no ping-pong)",
              back_hidden_after_return is True)

        # --- 5. Overlay toggle: aria-pressed, legend, wheel dimming --------
        page.goto(f"{base_url}/lifecycle.html#operate")
        page.wait_for_timeout(200)
        toggle = page.locator("#lc-overlay-toggle")
        check("overlay toggle starts unpressed", toggle.get_attribute("aria-pressed") == "false")
        toggle.click()
        page.wait_for_timeout(200)
        check("overlay toggle becomes pressed", toggle.get_attribute("aria-pressed") == "true")
        legend_hidden = page.evaluate("document.getElementById('lc-overlay-legend').hidden")
        check("overlay legend becomes visible", legend_hidden is False)
        counts_text = page.evaluate(
            "document.querySelector('#lc-overlay-legend .lc-overlay-counts').textContent")
        # Cross-checked by hand against lifecycle/links.csv during QA
        # (2026-09-25) for the Operate stage: Blocks 1, May impact 2,
        # Refers to 4.
        check("overlay legend counts match links.csv for Operate",
              counts_text.strip() == "Blocks 1 · May impact 2 · Refers to 4", counts_text)
        # Changing stage must reset the overlay back off.
        page.goto(f"{base_url}/lifecycle.html#optimize")
        page.wait_for_timeout(200)
        check("overlay resets to unpressed on a new stage",
              page.locator("#lc-overlay-toggle").get_attribute("aria-pressed") == "false")

        # --- 6. Fixed 2026-09-25 (found in exploratory QA the same day):
        # 'leads_to' links used to be completely dead — buildLinkList() and
        # computeAffected() were only ever called with rule/question ids,
        # never a stage id, so the three leads_to loops in links.csv never
        # rendered as anchors and were never counted in the overlay legend.
        # Both functions now also run against the current stage's own id.
        page.goto(f"{base_url}/lifecycle.html#optimize")
        page.wait_for_timeout(200)
        leads_to_anchors = page.evaluate(
            "[...document.querySelectorAll('.lc-link-anchor')]"
            ".filter(a => /Leads to|Led from/.test(a.textContent)).map(a => a.textContent)"
        )
        check("'leads_to' anchors render on the Optimize panel (optimize->plan, optimize->retire)",
              len(leads_to_anchors) == 2, leads_to_anchors)
        page.locator("#lc-overlay-toggle").click()
        page.wait_for_timeout(200)
        counts_text2 = page.evaluate(
            "document.querySelector('#lc-overlay-legend .lc-overlay-counts').textContent")
        # Cross-checked by hand against lifecycle/links.csv for Optimize: May
        # impact 3, Refers to 2, Leads to 2 (the two loop links out of optimize).
        check("overlay legend for Optimize now includes Leads to",
              counts_text2.strip() == "May impact 3 · Refers to 2 · Leads to 2", counts_text2)

        browser.close()

    print(f"\n{len(FAILURES)} failing check(s) out of the checks above.")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8935"
    sys.exit(main(url.rstrip("/")))
