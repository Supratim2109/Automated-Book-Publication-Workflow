from playwright.sync_api import sync_playwright

def scrape_website(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        page.screenshot(path="chapter_screenshot.png", full_page=True)
        content_element = page.locator("div.mw-parser-output").first
        content = content_element.inner_text()
        browser.close()
        return content
