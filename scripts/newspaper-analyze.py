#!/usr/bin/env python3
import argparse
import yaml
import datetime
import yaml
from munch import munchify

def main_function():
    """
    The main function for this script.
    """
    argument_parser, arguments = parse_arguments()
    
    load_config(arguments.config)
    
    if not execute_command(arguments):
        argument_parser.print_help()

def parse_arguments():
    """
    Parses the command-line arguments.
    """
    parser = argparse.ArgumentParser(description='Helps analyze articles.')
    parser.add_argument('--config', default='config.yaml',
        help='Configuration file for the options of this script')
    parser.add_argument('--search', default=None,
        help='Search for text in the articles')
    parser.add_argument('--list', default=None,
        help='List [title|authors|date|word-count|author|excerpt|content] of the articles')
    parser.add_argument('--sort', action='store_true',
        help='Sorts output (only applicable to --list).')
    parser.add_argument('--statistics', action='store_true',
        help='Gives basic statistics about the articles.')
    parser.add_argument('--count-articles', action='store_true',
        help='Counts the total number of articles')
    parser.add_argument('--count-words', action='store_true',
        help='Counts the total number of words')
    parser.add_argument('--count-paragraphs', action='store_true',
        help='Counts the total number of paragraphs')
    parser.add_argument('--count-by-author', action='store_true',
        help='Counts the number of articles by each author')
    parser.add_argument('--count-by-year', action='store_true',
        help='Counts the number of articles bucketed by year')
 
    return parser, parser.parse_args()

def load_config(config_path):
    """
    Loads the configuration file.
    """
    global config
    with open(config_path) as config_file:
        config = munchify(yaml.safe_load(config_file))

def execute_command(arguments):
    """
    Executes the command.
    """
    with open(config.paths.articles.data) as input_file:
        all_articles = yaml.safe_load(input_file)

        if arguments.search:
            search_articles(arguments.search, all_articles)
        elif arguments.list:
            list_property(arguments.list, all_articles, arguments.sort)
        elif arguments.statistics:
            show_statistics(all_articles)
        elif arguments.count_articles:
            count_articles(all_articles)
        elif arguments.count_words:
            count_words(all_articles)
        elif arguments.count_paragraphs:
            count_paragraphs(all_articles)
        elif arguments.count_by_author:
            count_by_author(all_articles)
        elif arguments.count_by_year:
            count_by_year(all_articles)
        else:
            return False
    
    return True

def show_statistics(all_articles):
    """
    Gives basic statistics.
    """
    print("BASIC STATISTICS")
    count_articles(all_articles)
    count_paragraphs(all_articles)
    count_words(all_articles)
    print()

    print("ARTICLES BY YEAR")
    count_by_year(all_articles)
    print()

    print("ARTICLES BY AUTHOR")
    count_by_author(all_articles)
    print()

def count_articles(all_articles):
    """
    Counts the total number of paragraphs written.
    """
    print(f"There are {len(all_articles)} articles.")

def count_paragraphs(all_articles):
    """
    Counts the total number of paragraphs written.
    """
    total_paragraphs = 0
    for title in all_articles:
        total_paragraphs += all_articles[title]['content'].count('\n')
    print(f"There are {total_paragraphs} paragraphs written.")

def count_words(all_articles):
    """
    Counts the total number of words written.
    """
    total_words = 0
    for title in all_articles:
        total_words += all_articles[title]['word-count']
    print(f"There are {total_words} words written.")

def count_by_year(all_articles):
    """
    Counts all the articles done each year.
    """
    all_dates = get_all_dates(all_articles)
    year_count = {}

    for date in all_dates:
        if date.year in year_count:
            year_count[date.year] += 1
        else:
            year_count[date.year] = 1

    print_all_items_in_dict(year_count)

def get_all_dates(all_articles):
    """
    Gets all the dates from the articles.
    """
    all_dates = []
    for title in all_articles:
        date_as_string = all_articles[title]['date']
        date_as_datetime = datetime.datetime.strptime(date_as_string, "%Y-%m-%dT%H:%M:%SZ")
        all_dates.append(date_as_datetime)
    return all_dates

def count_by_author(all_articles):
    """
    Gets the count of articles done by each author.
    """
    author_count = {}

    for title in all_articles:
        author = ", ".join(all_articles[title]['authors'])
        if author not in author_count:
            author_count[author] = 1
        else:
            author_count[author] = author_count[author] + 1
   
    print_all_items_in_dict(author_count)

def print_all_items_in_dict(all_items):

    # Find the length of the longest item.
    longest_item = 0
    for item in all_items:
        item_length = len(f"{item}")
        if item_length > longest_item:
            longest_item = item_length

    for item in sorted(all_items):
        print(f"{item}".rjust(longest_item) + f": {all_items[item]}")

def list_property(property, all_articles, sort):
    """
    Lists a given property.
    """
    contents = []
    for title in all_articles:
        try:
            contents.append(all_articles[title][property])
        except KeyError:
            valid_properties = ", ".join(all_articles[title].keys())
            print(f"'{property}' isn't a valid item to list.")
            print(f"Choices are: {valid_properties}")
            return
    
    # Sort in-place if applicable.
    if sort:
        contents.sort()
    
    # Print the output.
    for item in contents:
        print(item)

def search_articles(query, all_articles):
    """
    Searches the articles for a string.
    Case-insensitive.
    """
    articles_with_matches = 0
    total_matches = 0
    for title in all_articles:
        article_content = all_articles[title]["content"]
        matches = list(get_matches(query, article_content))

        if matches:
            print(f"{title}:")
            for snippet in matches:
                print(snippet)
            print()
            articles_with_matches += 1
            total_matches += len(matches)

    print(f"Found {total_matches} mentions of '{query}' in {articles_with_matches} articles.")

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