#worked with api request this code is not complete
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Step 1 & 2: Navigate and wait for the page to load
        print("Navigating to the product page...")
        await page.goto("https://www.walmart.com/ip/LEGO-Marvel-Guardians-of-the-Galaxy-Marvel-Rocket-Baby-Groot-Mini-Action-Figure-8-5/5015311522")
        await page.wait_for_selector('button:has-text("See all sellers")') # Wait for the button to appear

        graphql_response_data = None

        # Step 3: Listen for the specific GraphQL request
        async with page.expect_response(
            "https://www.walmart.com/orchestra/home/graphql/GetAllSellerOffers/**"
        ) as response_info:
            
            # Step 4: Simulate a human click to trigger the request
            print("Clicking the 'See all sellers' button to trigger the GraphQL request...")
            await page.click('button:has-text("See all sellers")')
            
            # Step 5: Wait for the response and get its body
            response = await response_info.value
            graphql_response_data = await response.json()
        
        print("\nGraphQL Response:")
        print(graphql_response_data)

        await browser.close()

asyncio.run(main())