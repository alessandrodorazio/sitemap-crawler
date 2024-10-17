from cat.mad_hatter.decorators import tool
import requests
import xml.etree.ElementTree as ET

def get_urls_from_sitemap(sitemap_url):
    """
    Given a sitemap URL, returns a list of every URL found within the sitemap.

    :param sitemap_url: A string representing the URL of the sitemap.
    :return: A list of URLs found in the sitemap.
    """
    try:
        # Fetch the sitemap content
        response = requests.get(sitemap_url)
        response.raise_for_status()

        # Parse the XML content
        root = ET.fromstring(response.content)

        # Extract URLs from the sitemap
        urls = []
        for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            loc_elem = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            if loc_elem is not None and loc_elem.text:
                urls.append(loc_elem.text)

        return urls

    except requests.RequestException as e:
        print(f"Error fetching sitemap: {e}")
        return []
    except ET.ParseError as e:
        print(f"Error parsing sitemap XML: {e}")
        return []

@tool(return_direct=True)  # default priority = 1
def add_urls_from_sitemap(url, cat):
    """Crawl a sitemap. Input is the sitemap url"""
    urls = get_urls_from_sitemap(url)
    for sitemap_url in urls:
        cat.rabbit_hole.ingest_file(cat, sitemap_url)
    return "Crawling started for " + url
