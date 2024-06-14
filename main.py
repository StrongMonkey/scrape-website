import os
import sys

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import hashlib


# Function to download a file from a URL
def download_file(url, folder):
    local_filename = os.path.join(folder, os.path.basename(urlparse(url).path.rstrip('/')))
    os.makedirs(os.path.dirname(local_filename), exist_ok=True)
    # Check if the file already exists to avoid downloading it again
    if os.path.exists(local_filename):
        print(f"File already exists: {local_filename}")
        return
    try:
        with requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, stream=True) as response:
            response.raise_for_status()
            with open(local_filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return
    print(f"Downloaded: {local_filename}")


# Function to recursively scrape the website
def scrape_website(url, base_url, visited, html_folder):
    if url in visited:
        return
    visited.add(url)

    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Failed to parse html content: {e}")
        return

    # Download the HTML file
    if not html_folder.endswith("/"):
        html_folder += "/"
    if url.endswith(".html"):
        html_filename = os.path.join(html_folder, urlparse(url).path.lstrip('/'))
    else:
        html_filename = os.path.join(html_folder, os.path.join(urlparse(url).path.lstrip('/'), "index.html"))

    os.makedirs(os.path.dirname(html_filename), exist_ok=True)
    with open(html_filename, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())
    print(f"Downloaded HTML: {html_filename}")

    # Find all links in the page
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(url, href)

        if full_url.endswith('.pdf'):
            return
        elif full_url.startswith(base_url):
            # Recursively scrape links within the same domain
            scrape_website(full_url, base_url, visited, html_folder)


def hash_string(input_string, algorithm='sha256'):
    # Create a new hash object using the specified algorithm
    hash_obj = hashlib.new(algorithm)

    # Encode the input string to bytes and update the hash object
    hash_obj.update(input_string.encode('utf-8'))

    # Get the hexadecimal digest of the hash
    return hash_obj.hexdigest()

# Main script
if __name__ == "__main__":
    base_url = sys.argv[1]
    html_folder = sys.argv[2]

    # Create directories if they do not exist
    os.makedirs(html_folder, exist_ok=True)
    os.makedirs(html_folder, exist_ok=True)

    visited = set()
    scrape_website(base_url, base_url, visited, html_folder)
