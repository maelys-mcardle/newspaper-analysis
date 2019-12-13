import urllib.request
import os.path
import os
import argparse
import hashlib
import yaml
from munch import munchify 

def main_function():
    """
    The main function for this script.
    """
    arguments = parse_arguments()

    load_config(arguments.config)

    url_list = extract_urls(config.paths.urls)

    download_files(url_list, config.paths.downloads)

def parse_arguments():
    """
    Parses the command-line arguments.
    """
    parser = argparse.ArgumentParser(description='Download the pages from an URL lists.')
    parser.add_argument('--config', default='config.yaml',
        help='Configuration file for the options of this script')

    return parser.parse_args()

def load_config(config_path):
    """
    Loads the configuration file.
    """
    global config
    with open(config_path) as config_file:
        config = munchify(yaml.safe_load(config_file))

def extract_urls(input_file_path):
    """
    Extracts all the URLs from an input file.
    """
    with open(input_file_path) as input_file:
        for line in input_file:
            yield line.strip()

def download_files(url_list, output_directory):
    """
    Downloads all the files from the url list.
    """

    create_output_directory(output_directory)

    for url in url_list:

        # Generate the output file path.
        url_hash = hash_url(url)
        output_file_path = os.path.join(output_directory, url_hash)

        # Download a file to that file path.
        download_file(url, output_file_path)

def create_output_directory(output_directory):
    """
    Creates the output directory if it doesn't exist.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

def hash_url(url):
    """
    Hashes the URL.
    """
    return hashlib.sha224(url.encode('utf-8')).hexdigest()

def download_file(url, output_file_path):
    """
    Downloads a single file from the url list.
    """
    print(f"Downloading: {url}")
    with open(output_file_path, 'w', encoding="utf-8") as output_file:
        request = urllib.request.Request(url)
        with urllib.request.urlopen(request) as web_page:
            page_content = web_page.read().decode('utf-8')
            output_file.write(page_content)

if __name__ == "__main__":
    main_function()