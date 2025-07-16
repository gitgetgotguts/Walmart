Walmart All Sellers Scraper

This asynchronous Python script uses curl_cffi to extract seller information for a specific Walmart item. It first loads the product page to collect necessary session cookies, then uses these to make a GraphQL API request for seller data.
What the Script Does

The script performs two main steps: loads a Walmart product page to establish a session and gather cookies (like userAppVersion), then uses that session to query a GraphQL API for all seller details.
Features

    Asynchronous: Uses asyncio for efficient requests.

    Session Management: Maintains cookies across requests.

    Browser Impersonation: Mimics a mobile Chrome browser.

    Dynamic Cookie: Extracts userAppVersion for API headers.

    Human-like Delays: Adds random pauses between steps.

Prerequisites

Python 3.7+ and the curl_cffi library.
Installation

pip install curl_cffi

Usage

    Save the script as walmart_scraper.py.

    Run from your terminal: python walmart_scraper.py

The script will print its progress and the JSON seller data if successful.
