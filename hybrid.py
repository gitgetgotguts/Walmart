import asyncio
from playwright.async_api import async_playwright
import curl_cffi
import json

async def playwright_get_cookies(url):
    """
    Uses Playwright to navigate a page and harvest all cookies generated
    by JavaScript, then returns them.
    """
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
        
        # Define the headers to mimic a legitimate browser
        headers = {
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

        
        context = await browser.new_context(
            user_agent=headers["User-Agent"],
            extra_http_headers=headers
        )
        
        page = await context.new_page()

        print("Playwright Phase: Navigating to the page to harvest cookies...")
        try:
            await page.goto(url, wait_until="domcontentloaded")
            print(f"Playwright navigation successful. URL: {page.url}")
            
            # Wait a few seconds to let all JavaScript, including the anti-bot script, run
            await page.wait_for_timeout(5000)
            
            # Extract all cookies from the browser context
            cookies = await context.cookies()
            print(f"Playwright harvested {len(cookies)} cookies.")
            
            await browser.close()
            return cookies
            
        except Exception as e:
            print(f"Playwright navigation failed. Error: {e}")
            await browser.close()
            return []


async def curl_cffi_make_request(cookies):
    """
    Uses curl_cffi to make the second request, injecting the harvested cookies.
    """
    session = curl_cffi.requests.AsyncSession()
    
    # Inject the cookies from Playwright into the curl_cffi session
    for cookie in cookies:
        session.cookies.set(
            cookie['name'],
            cookie['value'],
            domain=cookie['domain'],
            path=cookie['path']
        )
    
    print("\ncurl_cffi Phase: Making the GraphQL request...")
    url2 = "https://www.walmart.com/orchestra/home/graphql/GetAllSellerOffers/3f9fdc231f5f39017bebd11c8bb1266e9460f67addb2c880fa791802d873b630"
    params2 = {
        "variables": '{"itemId":"5015311522","isSubscriptionEligible":true,"conditionCodes":[1],"allOffersSource":"MORE_SELLER_OPTIONS"}'
    }
    
    headers2 = {
        "Host": "www.walmart.com",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "WM_MP": "true",
        "Content-Type": "application/json",
        "DNT": "1",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=4",
        "TE": "trailers"
    }

    try:
        response = await session.get(url2, params=params2, headers=headers2, impersonate="chrome131")
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            print("\nGraphQL Response:")
            print(response.text)
        else:
            print("Request failed. Response body:")
            print(response.text)
            
    except Exception as e:
        print(f"An error occurred during the curl_cffi request: {e}")
    finally:
        await session.close()


if __name__ == "__main__":
    # URL for the initial page load to get cookies
    product_url = "https://www.walmart.com/ip/LEGO-Marvel-Guardians-of-the-Galaxy-Marvel-Rocket-Baby-Groot-Mini-Action-Figure-8-5/5015311522"

    # Run the Playwright part to get cookies
    collected_cookies = asyncio.run(playwright_get_cookies(product_url))
    
    if collected_cookies:
        # Pass the cookies to the curl_cffi function to make the final request
        asyncio.run(curl_cffi_make_request(collected_cookies))
    else:
        print("Failed to collect cookies. Exiting.")