import asyncio
from playwright.async_api import async_playwright
import json

async def main():
    # Headers from the first curl_cffi request
    headers1 = {
        # "Host" is automatically managed by the browser
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        # "Accept-Encoding" is automatically managed by the browser
        "DNT": "1",
        "Sec-GPC": "1",
        # "Connection" is automatically managed by the browser
        "Referer": "https://www.youtube.com/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Priority": "u=0, i",
        # "TE" is automatically managed by the browser
    }

    async with async_playwright() as p:
        # Launch a browser with anti-detection arguments
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ]
        )
        
        # Create a new browser context with the specified headers
        context = await browser.new_context(
            user_agent=headers1["User-Agent"],
            extra_http_headers={k: v for k, v in headers1.items() if k != "User-Agent"}
        )
        
        page = await context.new_page()

        # The URL of the GraphQL endpoint we're interested in
        graphql_endpoint = "https://www.walmart.com/orchestra/home/graphql/GetAllSellerOffers"
        
        response_data = None
        
        async def handle_response(response):
            nonlocal response_data
            if graphql_endpoint in response.url and response.request.method == "GET":
                print(f"Captured GraphQL response from: {response.url}")
                try:
                    response_data =await response.json()
                except Exception as e:
                    print(f"Failed to read response body: {e}")
        
        page.on('response', handle_response)

        print("Navigating to the Walmart product page...")
        url1 = "https://www.walmart.com/ip/LEGO-Marvel-Guardians-of-the-Galaxy-Marvel-Rocket-Baby-Groot-Mini-Action-Figure-8-5/5015311522?athcpid=5015311522"
        
        try:
            await page.goto(url1, wait_until="domcontentloaded")
            print(f"Navigation successful. Current URL: {page.url}")
        except Exception as e:
            print(f"Navigation failed. The browser might be blocked. Error: {e}")
            await browser.close()
            return

        print("Waiting for the 'Compare all sellers' button to appear...")
        # Use a robust data attribute selector
        button_selector = 'button[data-dca-name="ItemBuyBoxOtherOptionsButton"]'
        
        try:
            # Wait for the button to be visible and ready to be clicked
            await page.wait_for_selector(button_selector, timeout=10000, state="visible")
            print("Button found. Clicking to trigger GraphQL request...")
            
            # Simulate a click on the button
            await page.click(button_selector)
            
            # Wait for a short time to allow the network request to complete
            await page.wait_for_timeout(5000)
            
        except Exception as e:
            print(f"Button not found within timeout or could not be clicked. Error: {e}")
        
        if response_data:
            print("\nSuccessfully captured GraphQL data!", response_data)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())