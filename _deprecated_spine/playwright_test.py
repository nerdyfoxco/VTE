from playwright.sync_api import sync_playwright

def test_playwright():
    print("Starting Playwright...")
    with sync_playwright() as p:
        print("Launching Chromium...")
        browser = p.chromium.launch(headless=False)
        print("Creating Context...")
        context = browser.new_context()
        print("Creating Page...")
        page = context.new_page()
        print("Navigating...")
        page.goto("https://www.google.com")
        print("Success!")
        browser.close()

if __name__ == "__main__":
    test_playwright()
