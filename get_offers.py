import asyncio
import random
import curl_cffi
import json
import argparse

async def main(product_url):
    # Initialize an AsyncSession
    # This session will persist cookies and connections across requests.
    session = curl_cffi.requests.AsyncSession()

    # --- Step 1: Make the initial GET request to the product page ---
    # url1 = "https://www.walmart.com/ip/LEGO-Marvel-Guardians-of-the-Galaxy-Marvel-Rocket-Baby-Groot-Mini-Action-Figure-8-5/5015311522"
    url1=product_url
    product_id=url1.split('/')[-1]
    params1 = {
        "athcpid": product_id,
    }
    headers1 = {
        "Host": "www.walmart.com",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "DNT": "1",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Referer": "https://www.youtube.com/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Priority": "u=0, i",
        "TE": "trailers",
    }

    print("Step 1: Making the initial request to collect cookies...")
    try:
        response1 = await session.get(
            url1,
            params=params1,
            headers=headers1,
            impersonate="chrome131_android"
        )
        print(f"Response 1 status code: {response1.status_code}")
    except Exception as e:
        print(f"An error occurred during the first request: {e}")
        return
    user_app_version_cookie = session.cookies.get('userAppVersion')

    delay = random.uniform(3, 7)
    print(f"Waiting for {delay:.2f} seconds to mimic human Browse...")
    await asyncio.sleep(delay)

    # --- Step 2: Make the GraphQL request using the same session ---
    url2 = "https://www.walmart.com/orchestra/home/graphql/GetAllSellerOffers/3f9fdc231f5f39017bebd11c8bb1266e9460f67addb2c880fa791802d873b630"
    params2 = {
        "variables": json.dumps({
            "itemId": product_id,
            "isSubscriptionEligible": True,
            "conditionCodes": [1],
            "allOffersSource": "MORE_SELLER_OPTIONS"
        })
    }
    headers2 = {
        "Host": "www.walmart.com",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": url1,
        "x-o-segment": "oaoh",
        "x-o-platform-version": user_app_version_cookie,
        "WM_MP": "true",
        "Content-Type": "application/json",
        "x-o-ccm": "server",
        "x-o-gql-query": "query GetAllSellerOffers",
        "X-APOLLO-OPERATION-NAME": "GetAllSellerOffers",
        "x-latency-trace": "1",
        "x-enable-server-timing": "1",
        "WM_PAGE_URL": url1,
        "baggage": "trafficType=customer,deviceType=desktop,renderScope=SSR,webRequestSource=Browser,pageName=itemPage",
        "x-o-platform": "rweb",
        "tenant-id": "elh9ie",
        "x-o-bu": "WALMART-US",
        "x-o-mart": "B2C",
        "DNT": "1",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=4",
        "TE": "trailers"
    }

    print("\nStep 2: Making the GraphQL request using the same session...")
    try:
        response2 = await session.get(
            url2,
            params=params2,
            headers=headers2,
            impersonate="chrome131_android"
        )
        print(f"Response 2 status code: {response2.status_code}")
        
        if response2.status_code == 200:
            json_data = response2.json()
            output_filename = f"{product_id}.json"
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)
            print(f"\nSuccessfully saved GraphQL response to {output_filename}")

        else:
            print("GraphQL request failed. The response text might contain a captcha or block page.")
            print(response2.text())

    except Exception as e:
        print(f"An error occurred during the second request: {e}")
    finally:
        await session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get all seller information for a Walmart item."
    )
    parser.add_argument(
        "url",
        type=str,
        help="The full URL of the Walmart product page (e.g., https://www.walmart.com/ip/...).",
    )

    args = parser.parse_args() 

    asyncio.run(main(args.url))