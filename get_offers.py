import asyncio
import random
import curl_cffi

async def main():
    # Initialize an AsyncSession
    # This session will persist cookies and connections across requests.
    session = curl_cffi.requests.AsyncSession()

    # --- Step 1: Make the initial GET request to the product page ---
    url1 = "https://www.walmart.com/ip/LEGO-Marvel-Guardians-of-the-Galaxy-Marvel-Rocket-Baby-Groot-Mini-Action-Figure-8-5/5015311522"
    params1 = {
        "athcpid": "5015311522",
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

    delay = random.uniform(3, 7)
    print(f"Waiting for {delay:.2f} seconds to mimic human Browse...")
    await asyncio.sleep(delay)

    # --- Step 2: Make the GraphQL request using the same session ---
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
        "Referer": url1,
        "x-o-segment": "oaoh",
        "x-o-platform-version": "usweb-1.212.0-3d45d91d0379181242084b528eb8317750d32b99-7102008r",
        "x-o-correlation-id": "DTMSJnTrT-fB-Y6g5GkifXuIZCbr7UFPP6P3",
        "wm_qos.correlation_id": "DTMSJnTrT-fB-Y6g5GkifXuIZCbr7UFPP6P3",
        "WM_MP": "true",
        "Content-Type": "application/json",
        "x-o-ccm": "server",
        "x-o-gql-query": "query GetAllSellerOffers",
        "X-APOLLO-OPERATION-NAME": "GetAllSellerOffers",
        "x-latency-trace": "1",
        "x-enable-server-timing": "1",
        "traceparent": "00-1852a180bc90715bd6826a1cee6fac4a-29242591928644cf-00",
        "WM_PAGE_URL": url1,
        "baggage": "trafficType=customer,deviceType=desktop,renderScope=SSR,webRequestSource=Browser,pageName=itemPage,isomorphicSessionId=IWPiIAnO15Bk1vPG6osjB,renderViewId=38543792-21e7-485f-aefd-d959d856275d",
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
            print("\nGraphQL Response:")
            print(response2.json())
        else:
            print("GraphQL request failed. The response text might contain a captcha or block page.")
            print(response2.text())

    except Exception as e:
        print(f"An error occurred during the second request: {e}")
    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())