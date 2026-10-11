"""Render a URL in a real browser and print the document to stdout.

This replaces `chrome --dump-dom`, which no longer works on the Chromium build
Playwright installs: on build 1243 it emits nothing for even a
`data:text/html,<h1>hi</h1>` URL and then hangs instead of exiting, so every
call to it timed out with an empty document. Driving the browser through
Playwright removes the version guesswork, and it is the same API the Python
render gate (`tests/ci/test_workbench_renders.py`) already uses.

Python is the driver rather than Node because the CI job installs the Python
Playwright package for its browser step, while `playwright` is not a dependency
of the Studio's npm package and adding it would mean regenerating the lockfile
for a test-only tool.

Usage: python3 dom_dump.py <url>
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: dom_dump.py <url>\n")
        return 2
    url = sys.argv[1]
    timeout_ms = int(os.environ.get("APPGEN_STUDIO_DUMP_TIMEOUT_MS", "60000"))

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.stderr.write(
            "The `playwright` Python package is not installed. Install it with "
            "`python -m pip install playwright` and then "
            "`python -m playwright install chromium`.\n"
        )
        return 1

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=os.environ.get("APPGEN_CHROME_BIN") or None,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        try:
            page = browser.new_page()
            page.set_default_timeout(timeout_ms)
            # The Studio fetches every panel from `/api/studio/*`, so the
            # document is complete only once those requests have settled.
            # `load` fires while the panels are still empty.
            page.goto(url, wait_until="networkidle", timeout=timeout_ms)
            sys.stdout.write(page.content())
        finally:
            browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
