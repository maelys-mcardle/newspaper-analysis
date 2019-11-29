import argparse
import yaml

def main_function():
    """
    The main function for this script.
    """
    argument_parser, arguments = parse_arguments()

    if arguments.search:
        execute_command(arguments)
    else:
        argument_parser.print_help()

def parse_arguments():
    """
    Parses the command-line arguments.
    """
    parser = argparse.ArgumentParser(description='Download the pages from an URL lists.')
    parser.add_argument('--input-file', default='all-articles-with-metadata.yaml',
        help='Input file for the parsed pages')
    parser.add_argument('--search', default=None,
        help='Text to search in the articles')

    return parser, parser.parse_args()

def execute_command(arguments):

    with open(arguments.input_file) as input_file:
        articles_and_metadata = yaml.safe_load(input_file)

        if arguments.search:
            search_articles(arguments.search, articles_and_metadata)


def search_articles(query, articles_and_metadata):
    """
    Searches the articles for a string.
    """
    results = 0
    for title in articles_and_metadata:
        article_content = articles_and_metadata[title]["content"]
        if query in article_content:
            show_snippet(query, title, article_content)
            results += 1

    print(f"Found {results} results.")

def show_snippet(query, title, content):
    """
    Show a text snippet.
    """

    margin = 10
    query_len = len(query)
    content_len = len(content)
    
    match_start = content.find(query)
    match_end = match_start + query_len
    snippet_start = match_start - margin if match_start - margin >= 0 else 0
    snippet_end = match_end + margin if match_end + margin < content_len else content_len - 1

    print(f"{title}:")
    print(f"   ...{content[snippet_start:snippet_end]}...")

if __name__ == "__main__":
    main_function()