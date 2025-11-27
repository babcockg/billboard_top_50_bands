import asyncio
import aiohttp
import ssl
from bs4 import BeautifulSoup
import time
import os

async def fetch_html(session, url):
    """Fetches the HTML content of a given URL asynchronously."""
    async with session.get(url) as response:
        # Read the response body as text
        return await response.text()


def parse_html(html):
    """Parses HTML content using BeautifulSoup (synchronous operation)."""
    # Beautiful Soup parsing is CPU-bound and runs synchronously
    soup = BeautifulSoup(html, "lxml")  # Using 'lxml' parser for performance
    bands = soup.find_all("h2", class_=False)
    return bands


async def fetch_and_parse(session, url):
    """Combines fetching and parsing for a single URL."""
    html = await fetch_html(session, url)
    # Perform the synchronous parsing step
    return parse_html(html)


async def scrape_urls(urls):
    """Manages the asynchronous scraping of multiple URLs."""
    start_time = time.time()

    # Create SSL context with certificate verification
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Create connector with SSL context
    connector = aiohttp.TCPConnector(ssl=ssl_context)

    # Create a single aiohttp session for efficient connection reuse
    async with aiohttp.ClientSession(connector=connector) as session:
        # Create a list of tasks for asyncio.gather
        tasks = [fetch_and_parse(session, url) for url in urls]
        # Run all tasks concurrently and gather results as they complete
        results = await asyncio.gather(*tasks)

    end_time = time.time()
    print(f"Scraping completed in {end_time - start_time:.2f} seconds")
    return results


# List of URLs to scrape
urls_list = [
    "https://www.billboard.com/lists/best-rock-bands/"
]

# Run the main asynchronous function
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    results = asyncio.run(scrape_urls(urls_list))
    leading_spaces = 2
    for result in results[0]:
        period_position = result.string.find(".")
        print(f"{' '* (leading_spaces - period_position)} {result.string}")

