"""Gets screenshots of thread comments"""

import os
import json
from playwright.sync_api import sync_playwright, ViewportSize
from dotenv import load_dotenv

load_dotenv()

def get_screenshots(thread):
    """Gets screenshots of the thread"""

    path = f"assets/subreddits/{thread['subreddit']}/{thread['id']}/screenshots"
    os.mkdir(path)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()

        cookie = open("./data/cookie-dark-mode.json", encoding="utf-8")
        cookie = json.load(cookie)
        context.add_cookies(cookie)

        page = context.new_page()

        # Login if thread is NSFW
        if thread['over_18']:
            print('Logging in...')
            page.goto("https://reddit.com/login")

            page.locator("input[name='username']").fill(os.getenv("REDDIT_USERNAME"))
            page.locator("input[name='password']").fill(os.getenv("REDDIT_PASSWORD"))
            page.get_by_role("button", name="Log in").click()

            page.wait_for_load_state('networkidle')

        page.goto(thread["url"], timeout=0)
        page.set_viewport_size(ViewportSize(width=1920, height=1080))

        # If the thread is NSFW
        if page.locator('[data-testid="content-gate"]').is_visible():
            page.locator('[data-testid="content-gate"] button').click()
            page.wait_for_load_state()

            if page.locator('[data-click-id="text"] button').is_visible():
                page.locator('[data-click-id="text"] button').click()

        page.locator('[data-test-id="post-content"] > [data-adclicklocation="title"]').screenshot(
            path=f"{path}/title.png"
        )

        if thread["body"]:
            page.locator('[data-adclicklocation="media"]').screenshot(
                path=f"{path}/body.png"
            )

        for comment in thread["comments"]:
            page.goto(comment["url"], timeout=0)

            if page.locator('[data-testid="content-gate"]').is_visible():
                page.locator('[data-testid="content-gate"] button').click()

            page.locator(f'#t1_{comment["id"]}').screenshot(
                path=f"{path}/{comment['id']}.png"
            )
