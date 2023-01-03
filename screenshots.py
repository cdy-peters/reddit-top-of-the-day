"""Gets screenshots of thread comments"""

import os
import json
from playwright.sync_api import sync_playwright, ViewportSize


def get_screenshots(thread):
    """Gets screenshots of the thread"""

    os.mkdir(f"assets/threads/{thread['id']}/screenshots")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()

        cookie = open("./cookie-dark-mode.json", encoding="utf-8")
        cookie = json.load(cookie)
        context.add_cookies(cookie)

        page = context.new_page()
        page.goto(thread["url"], timeout=0)
        page.set_viewport_size(ViewportSize(width=1920, height=1080))

        # If the thread is NSFW
        if page.locator('[data-testid="content-gate"]').is_visible():
            page.locator('[data-testid="content-gate"] button').click()
            page.wait_for_load_state()

            if page.locator('[data-click-id="text"] button').is_visible():
                page.locator('[data-click-id="text"] button').click()

        page.locator('[data-adclicklocation="title"]').screenshot(
            path=f"assets/threads/{thread['id']}/screenshots/title.png"
        )
        page.locator('[data-adclicklocation="media"]').screenshot(
            path=f"assets/threads/{thread['id']}/screenshots/body.png"
        )

        for i, comment in enumerate(thread["comments"]):
            page.goto(comment["url"], timeout=0)

            if page.locator('[data-testid="content-gate"]').is_visible():
                page.locator('[data-testid="content-gate"] button').click()

            page.locator(f'#t1_{comment["id"]}').screenshot(
                path=f"assets/threads/{thread['id']}/screenshots/{comment['id']}.png"
            )
