import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Check Actions
        print("Checking Actions...")
        try:
            await page.goto("https://github.com/nerdyfoxco/VTE/actions", timeout=30000)
            await page.wait_for_load_state("networkidle")
            await page.screenshot(path="actions_status.png")
            print("Captured actions_status.png")
            
            # Extract Latest Run Status
            # Look for the first row in the workflow runs list
            # GitHub uses aria-labels on the status icons
            
            # approximate selector for the first run's status icon
            # It usually is inside a Box-row
            try:
                # Wait for at least one run to appear
                await page.wait_for_selector(".Box-row", timeout=5000)
                
                # Get the first icon's label
                # formatting might vary, usually path or svg has aria-label
                # Let's get the text of the first row to identify the run name
                first_row_text = await page.inner_text(".Box-row >> nth=0")
                print(f"Latest Run Info: {first_row_text}")
                
                # Try to find specific status text/icon
                status_icon_label = await page.get_attribute(".Box-row >> nth=0 >> svg", "aria-label")
                if status_icon_label:
                    print(f"Latest Run Status Icon: {status_icon_label}")
                else:
                     # Fallback to searching for specific status classes/icons if aria-label missing
                     html = await page.inner_html(".Box-row >> nth=0")
                     if "octicon-check" in html:
                         print("Latest Run Status: Success (Icon Check)")
                     elif "octicon-x" in html:
                         print("Latest Run Status: Failure (Icon X)")
                     elif "octicon-stop" in html or "octicon-dot-fill" in html:
                          print("Latest Run Status: In Progress/Queued")
                     else:
                          print("Latest Run Status: Unknown Icon")

            except Exception as e:
                print(f"Could not extract specific run status: {e}")
                
        except Exception as e:
            print(f"Error checking Actions: {e}")

        # Check Dependabot
        print("Checking Dependabot...")
        try:
            await page.goto("https://github.com/nerdyfoxco/VTE/security/dependabot", timeout=30000)
            await page.wait_for_load_state("networkidle")
            await page.screenshot(path="dependabot_status.png")
            print("Captured dependabot_status.png")
        except Exception as e:
            print(f"Error checking Dependabot: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
