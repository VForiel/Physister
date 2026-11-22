"""Captures d'écran pour vérifier le rendu : python tests/screenshot.py URL_PATH [SORTIE] [--dark]."""

import sys

from playwright.sync_api import sync_playwright

path = sys.argv[1] if len(sys.argv) > 1 else ""
out = sys.argv[2] if len(sys.argv) > 2 else "shot.png"
dark = "--dark" in sys.argv
width = 420 if "--mobile" in sys.argv else 1400

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": width, "height": 1000},
                      color_scheme="dark" if dark else "light")
    page.goto(f"http://localhost:8599/{path}")
    page.wait_for_selector("[data-testid='stAppViewContainer']", timeout=30000)
    page.wait_for_timeout(5000)
    page.screenshot(path=out, full_page=True)
    b.close()
