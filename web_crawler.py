import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import os

class WebCrawler:
    def __init__(self, start_url, max_depth=2, delay=1.0):
        self.start_url = start_url
        self.max_depth = max_depth
        self.delay = delay
        self.visited = set()
        self.output_dir = "crawled_pages"
        os.makedirs(self.output_dir, exist_ok=True)

    def save_page(self, url, content):
        """Save the page content to a file."""
        filename = os.path.join(self.output_dir, urlparse(url).netloc + "_" + str(hash(url)) + ".html")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved: {url} to {filename}")

    def get_links(self, soup, base_url):
        """Extract all valid links from the page."""
        links = set()
        for anchor in soup.find_all("a", href=True):
            href = anchor["href"]
            full_url = urljoin(base_url, href)
            parsed = urlparse(full_url)
            if parsed.scheme in ["http", "https"] and parsed.netloc:
                links.add(full_url)
        return links

    def crawl(self, url, depth=0):
        """Recursively crawl the web starting from the given URL."""
        if depth > self.max_depth or url in self.visited:
            return

        print(f"Crawling: {url} (Depth: {depth})")
        self.visited.add(url)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Save the page content
            self.save_page(url, response.text)

            # Get links and crawl them
            links = self.get_links(soup, url)
            for link in links:
                if link not in self.visited:
                    time.sleep(self.delay)  # Respectful delay
                    self.crawl(link, depth + 1)

        except requests.RequestException as e:
            print(f"Failed to crawl {url}: {e}")

def main():
    start_url = input("Enter the starting URL (e.g., https://example.com): ")
    max_depth = int(input("Enter the maximum crawl depth (e.g., 2): "))
    crawler = WebCrawler(start_url, max_depth)
    crawler.crawl(start_url)

if __name__ == "__main__":
    main()