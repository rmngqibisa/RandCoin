from playwright.sync_api import sync_playwright

def verify_site():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto("http://localhost:8000")
            print("Page title:", page.title())

            # Wait a bit for animations
            page.wait_for_timeout(2000)

            # Take screenshot
            page.screenshot(path="website_screenshot.png", full_page=True)
            print("Screenshot saved to website_screenshot.png")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_site()
