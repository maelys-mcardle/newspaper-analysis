from bs4 import BeautifulSoup
import argparse
import json
from os import listdir
from os.path import isfile, join
import yaml

def main_function():
    """
    The main function for this script.
    """
    arguments = parse_arguments()

    input_files = get_input_files(arguments.input_directory)

    input_articles = parse_all_files(input_files)

    write_output_files(input_articles, arguments.output_yaml_file, arguments.output_markdown_file)

def parse_arguments():
    """
    Parses the command-line arguments.
    """
    parser = argparse.ArgumentParser(description='Parses the downloaded pages to enable analysis.')
    parser.add_argument('--input-directory', default='downloads',
        help='Input directory for the downloaded pages')
    parser.add_argument('--output-yaml-file', default='all-articles-with-metadata.yaml',
        help='Output file for the parsed pages')
    parser.add_argument('--output-markdown-file', default='all-articles.md',
        help='Output file for the parsed pages')

    return parser.parse_args()

def get_input_files(input_directory):
    """
    Gets all the files from the input directory.
    """

    for possible_file_entry in listdir(input_directory):
        possible_file_path = join(input_directory, possible_file_entry)
        if isfile(possible_file_path):
            yield possible_file_path

def parse_all_files(input_file_paths):
    """
    Parses all the files to extract their articles.
    """
    for file_path in input_file_paths:
        with open(file_path, encoding="utf8") as html_file:
            article = extract_article(html_file)
            yield article

def write_output_files(input_articles, yaml_file_path, markdown_file_path):
    """
    Writes the files to output.
    """
    with open(yaml_file_path, 'w', encoding="utf-8") as yaml_file:
        with open(markdown_file_path, 'w', encoding="utf-8") as markdown_file:
            for article in input_articles:
                # Turn the content from an array of paragraphs to a single text.
                article["content"] = "\n".join(article["content"])

                # Write to the files.
                write_to_yaml_file(yaml_file, article)
                write_to_markdown_file(markdown_file, article)

def extract_article(html_file):
    """
    Extracts the metadata for the article.
    These are contained in <script type="application/json" id="page-data">
    """

    # Extract the JSON stored in the page-data element.
    parsed_html = BeautifulSoup(html_file, 'html.parser')
    page_data = parsed_html.find("script", {"id": "page-data"})

    if page_data:
        raw_json = page_data.get_text()
        metadata = json.loads(raw_json)

        return {
            "title": metadata["page"]["title"]["main"],
            "date": metadata["page"]["date"]["pub"],
            "authors": metadata["page"]["authors"],
            "excerpt": metadata["page"]["excerpt"] if "excerpt" in metadata["page"] else None,
            "word-count": metadata["page"]["wc"],
            "content": extract_article_content(parsed_html)
        }

def extract_article_content(parsed_html):
    """
    Extracts each paragraph from the article content.
    Article body is contained in <div class="story-content" itemprop="articleBody">
    """

    # Load paragraphs.
    paragraphs = []
    for article_body in parsed_html.find_all(itemprop="articleBody"):
        for paragraph in article_body.find_all('p'):
            if not paragraph.find_parent('blockquote'):
                paragraph_text = paragraph.get_text()
                sanitized_paragraph = sanitize_paragraph(paragraph_text)
                paragraphs.append(sanitized_paragraph)
    
    # Remove empty paragraphs.
    paragraphs = [i for i in paragraphs if i] 

    return paragraphs


def sanitize_paragraph(paragraph):
    """
    Remove undesired elements from the paragraph.
    This includes removing [np_storybar] and [np-related] pseudo-elements.
    """
    paragraph = strip_pseudo_tag("np_storybar", paragraph)
    paragraph = paragraph.replace("[np-related]", "")
    return paragraph

def strip_pseudo_tag(tag_name, paragraph):
    """
    Strips a pseudo-tag from a paragarph.
    """

    cleansed_paragraph = ""
    start = paragraph.find(f"[{tag_name}")
    end = paragraph.find(f"[/{tag_name}]")

    if (start == -1 and end == -1):
        cleansed_paragraph = paragraph
    else:
        if (start >= 0):
            cleansed_paragraph += paragraph[:start]

        if (end >= 0):
            cleansed_paragraph += paragraph[end + len(f"[/{tag_name}]"):]
    
    return cleansed_paragraph

def write_to_yaml_file(yaml_file, article):
    """
    Writes the article object to the yaml file.
    """
    yaml.dump({article["title"]: article}, yaml_file)

def write_to_markdown_file(markdown_file, article):
    """
    Writes the article object to the yaml file.
    """
    markdown_file.write(
        f"# {article['title']}\n" +
        f"{article['content']}\n")

if __name__ == "__main__":
    main_function()