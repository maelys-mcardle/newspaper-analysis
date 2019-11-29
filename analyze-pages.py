import argparse
import yaml

def main_function():
    """
    The main function for this script.
    """
    argument_parser, arguments = parse_arguments()

    ran_command = execute_command(arguments)

    if not ran_command:
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
    parser.add_argument('--list', default=None,
        help='List [title|authors|date|word-count|author|excerpt|content] of the articles')

    return parser, parser.parse_args()

def execute_command(arguments):
    """
    Executes the command.
    """
    with open(arguments.input_file) as input_file:
        articles_and_metadata = yaml.safe_load(input_file)

        if arguments.search:
            search_articles(arguments.search, articles_and_metadata)
        elif arguments.list:
            list_property(arguments.list, articles_and_metadata)
        else:
            return False
    
    return True

def list_property(property, articles_and_metadata):
    """
    Lists a given property.
    """
    for title in articles_and_metadata:
        try:
            print(articles_and_metadata[title][property])
        except KeyError:
            valid_properties = ", ".join(articles_and_metadata[title].keys())
            print(f"'{property}' isn't a valid item to list.")
            print(f"Choices are: {valid_properties}")
            return

def search_articles(query, articles_and_metadata):
    """
    Searches the articles for a string.
    Case-insensitive.
    """
    results = 0
    for title in articles_and_metadata:
        article_content = articles_and_metadata[title]["content"]
        matches = list(get_matches(query, article_content))

        if matches:
            print(f"{title}:")
            for snippet in matches:
                print(snippet)
            print()
            results += 1

    print(f"Found {results} results.")

def get_matches(query, content):
    """
    Show snippets for the matches.
    """

    margin = 30
    query_len = len(query)
    content_len = len(content)
    match_start = -1

    while True:
        match_start = content.upper().find(query.upper(), match_start + 1)

        if match_start == -1:
            break

        match_end = match_start + query_len
        snippet_start = match_start - margin if match_start - margin >= 0 else 0
        snippet_end = match_end + margin if match_end + margin < content_len else content_len - 1

        snippet = content[snippet_start:snippet_end].replace("\n", " ")
        yield f"   ...{snippet}..."

if __name__ == "__main__":
    main_function()