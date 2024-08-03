import requests

from bs4 import BeautifulSoup
from datetime import date
from urllib.parse import urljoin, urlparse


def crawl_site_to_fetch_urls(
        start_url, 
        min_length_text_body=1000, 
        max_number_visited_urls=None, 
        max_number_qualified_urls=None,
        visited_urls=[],
        urls_to_visit=[]
    ):
    """
    Crawl the given website starting from start_url and collect all unique page URLs within the same domain
    that have a body text content longer than the specified min_length_text_body.
    
    Parameters:
    - start_url (str): The starting URL to begin crawling from.
    - min_length_text_body (int): Minimum length of the text content in the body to include the URL in the result.
    - max_number_visited_urls (int, optional): Maximum number of URLs to visit.
    - max_number_qualified_urls (int, optional): Maximum number of URLs to return.
    - visited_urls (set, optional): Set of URLs that have been visited.
    - urls_to_visit (list, optional): Set of URLs that have been visited. If none, it's set as start_url, otherwise, start_url is ignored.

    Returns:
    - list: URLs meeting the text content length requirement.
    """
    n_visited_urls_previously = len(visited_urls)
    visited_urls = set(visited_urls)
    
    if not urls_to_visit:
        urls_to_visit = [start_url]
    urls_to_visit = urls_to_visit.copy()

    base_domain = urlparse(start_url).netloc
    qualifying_urls = set()

    while urls_to_visit:
        current_url = urls_to_visit.pop(0)

        if current_url in visited_urls:
            continue

        visited_urls.add(current_url)

        try:
            response = requests.get(current_url)
            response.raise_for_status()  # Ensure the request was successful
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text from the <body> tag, excluding script and style elements
            text = soup.body.get_text(separator=' ', strip=True) if soup.body else ""
            text = ' '.join(text.split())  # Normalize whitespace

            if len(text) >= min_length_text_body:
                qualifying_urls.add(current_url)

            # Find and process all hyperlinks within the same domain
            for link in soup.find_all('a', href=True):
                full_url = urljoin(current_url, link['href'])
                if urlparse(full_url).netloc == base_domain \
                    and full_url[-1] == '/' \
                    and full_url not in visited_urls \
                    and full_url not in urls_to_visit:
                    urls_to_visit.append(full_url)

        except requests.RequestException as e:
            print(f"Failed to fetch {current_url}: {e}")

        if max_number_visited_urls and len(visited_urls)-n_visited_urls_previously >= max_number_visited_urls:
            break

        if max_number_qualified_urls and len(qualifying_urls) >= max_number_qualified_urls:
            break

    return list(qualifying_urls), list(visited_urls), urls_to_visit


def parse_collected_web_data(qualified_urls, visited_urls, urls_to_visit, visited_urls_previously=[], urls_to_visit_previously=[]):
    # Get today's date and format the date as YYYY-MM-DD
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")

    old_urls_visited = [url for url in visited_urls if url in urls_to_visit_previously]
    new_urls_visited = [url for url in visited_urls if url not in visited_urls_previously+urls_to_visit_previously]
    new_urls_to_visit = [url for url in urls_to_visit if url not in urls_to_visit_previously]
    urls = old_urls_visited + new_urls_visited + new_urls_to_visit

    is_new = [True if url not in old_urls_visited else False for url in urls]
    is_visited = [True if url in visited_urls else False for url in urls]
    is_qualified = [True if url in qualified_urls else False for url in urls]
    visited_date = [today_str if url in visited_urls else None for url in urls]
    is_to_ingest = is_qualified

    web_data_to_update = []
    web_data_to_add = []
    for url, new, iv, vd, iq, ii in  zip(urls, is_new, is_visited, visited_date, is_qualified, is_to_ingest):
        data = {
            'url': url,
            'is_visited': iv,
            'visited_date': vd,
            'is_qualified': iq,
            'is_to_ingest': ii,
        }
        if new:
            web_data_to_add.append(data)
        else:
            web_data_to_update.append(data)

    return web_data_to_update, web_data_to_add
