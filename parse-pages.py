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

    # Load element that contains the story.
    article_body = parsed_html.find(itemprop="articleBody")

    # Remove all blockquotes, figures, etc.
    delete_elements(article_body, [
        ("blockquote", {}),
        ("figure", {}),
        ("ul", {"class": "related_links"}),
        ("div", {"class": "pullquote-share-container"}),
        ("script", {})])

    # Append a newline after <p> and <br> tags.
    append_newline_after_elements(article_body, ["br", "p"])

    # Extract the text.
    article_content = article_body.get_text(separator=" ")

    # Remove national post pseudo-elements
    article_content = delete_pseudo_elements(article_content)

    # Split text into paragraphs.
    paragraphs = article_content.split("\n")

    # Remove empty paragraphs and strip whitespace.
    paragraphs = [i.strip() for i in paragraphs if i.strip()]
    
    return paragraphs

def delete_elements(article, elements_to_delete):
    """
    Deletes the elements.
    """
    for tag, attributes in elements_to_delete:
        for found_element in article.find_all(tag, attributes):
            found_element.decompose()

def append_newline_after_elements(article, elements_to_append):
    """
    Appends a newline after these elements.
    """
    for tag in elements_to_append:
        for matching_element in article.find_all(tag):
            matching_element.replace_with(matching_element.text + "\n")

def delete_pseudo_elements(article):
    """
    Removes the pseudo elements from the article.
    """

    # Remove the np_storybar. There could be many matches
    # per article, so iterate over them.
    remove_next_pseudo_tag = True
    while remove_next_pseudo_tag:
        remove_next_pseudo_tag, article = strip_pseudo_tag("np_storybar", article)

    article = article.replace("[np-related]", "")
    return article

def strip_pseudo_tag(tag_name, original_paragraph):
    """
    Strips a pseudo-tag from a paragraph.
    """

    cleansed_paragraph = ""
    found_match = False
    start_of_opening_tag = original_paragraph.find(f"[{tag_name}")
    start_of_closing_tag = original_paragraph.find(f"[/{tag_name}]")

    # Did not find closing/opening tag.
    if (start_of_opening_tag == -1 and start_of_closing_tag == -1):
        cleansed_paragraph = original_paragraph
        found_match = False

    # Found a closing or opening tag.
    else:
        # Indicate match was found.
        found_match = True

        # Grab everything before the opening tag, if there's anything there.
        if (start_of_opening_tag > 0):
            cleansed_paragraph += original_paragraph[:start_of_opening_tag]

        # Grab everything after the closing tag, if there's anything there.
        end_of_closing_tag = start_of_closing_tag + len(f"[/{tag_name}]")
        if (start_of_closing_tag >= 0 and end_of_closing_tag < len(original_paragraph) - 1):
            cleansed_paragraph += original_paragraph[end_of_closing_tag:]

    return found_match, cleansed_paragraph

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