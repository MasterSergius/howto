#!/usr/bin/python3

import click

from result_handler import SearchResult, find_command


@click.option('-t', '--tags', help='Search by tags only', is_flag=True)
@click.option('-n', '--name', help='Search by name only', is_flag=True)
@click.argument('howto', nargs=-1)
@click.command()
def main(name, tags, howto):
    user_input = ' '.join(howto)
    find_command(user_input)

if __name__ == '__main__':
    main()
