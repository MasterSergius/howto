#!/usr/bin/python3

import click

from result_handler import SearchResult, find_command


def print_search_result(result):
    click.echo(f'Description: {result.descriptions}')
    click.echo(f'Command syntax: {result.command}')
    click.echo(f'Example: {result.example}')
    click.echo(f'match score (for debugging): {result.score}')


def print_results(results):
    for result in results:
        print_search_result(result)
        click.echo()


@click.option('-t', '--tags', help='Search by tags only', is_flag=True)
@click.option('-n', '--name', help='Search by name only', is_flag=True)
@click.argument('howto', nargs=-1)
@click.command()
def main(name, tags, howto):
    user_input = ' '.join(howto)
    results = find_command(user_input)
    if len(results) == 0:
        click.echo('No matches')
    else:
        print_results(results)

if __name__ == '__main__':
    main()
