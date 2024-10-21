"""
__author__ = "Paul Waldecker"
__email__ = "0157@htl.rennweg.at"
__version__ = "3.0"
__copyright__ = "Copyright 2024"
__license__ = "GPL"
__status__ = "Ready to Review"
"""
import argparse
from dateutil import parser
import subprocess
import sys

from matplotlib import pyplot as plt


def run_git_log(author, path, verbose):
    """
    Diese Funktion führt ein git log command aus und gibt die Ausgabe zurück
    :param author: Der author des git repositories
    :param path: Der absolute Pfad zum git repository
    :param verbose: ob verbose oder nicht
    :return: Gib die Ausgabe des git log commands zurück
    """
    git_command = ['git', 'log', '--pretty=%an;%ad---END---', '--date=rfc']

    if author:
        git_command.insert(2, '--author={}'.format(author))

    if path:
        git_command.insert(1, '-C')
        git_command.insert(2, path)

    if verbose:
        print(f"Running command: {' '.join(git_command)}")

    try:
        process = subprocess.Popen(git_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Error running git log: {stderr.decode('utf-8')}")
            sys.exit(1)

        return stdout.decode('utf-8')
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def parse_git_log(output):
    """
    Diese Funktion parst die Ausgabe des git log commands
    :param output: Git log command output
    :return: Bereiningte Ausgabe des git log commands
    """
    commits = output.split('---END---')
    parsed_commits = []

    for commit in commits:
        if commit.strip():
            author, date = commit.split(';')
            parsed_commits.append({'author': author.strip(), 'date': date.strip()})

    return parsed_commits


def calculate_commit_counts(parsed_commits):
    """
    Diese Funktion berechnet die Anzahl der Commits pro Wochentag und Uhrzeit
    :param parsed_commits: nimmt als Input die bereinigte Ausgabe des git log commands
    :return: Gib die Anzahl der Commits pro Wochentag und Uhrzeit zurück
    """
    commit_counts = {}

    for commit in parsed_commits:
        commit_date = parser.parse(commit['date'])
        weekday = commit_date.weekday()
        hour = commit_date.hour
        key = (weekday, hour)

        if key not in commit_counts:
            commit_counts[key] = 0

        commit_counts[key] += 1

    return commit_counts


def create_plot(commit_counts, author, filename=None):
    """
    Diese Funktion erstellt ein Plot mit den Commit Daten
    :param commit_counts: Anzahl der Commits pro Wochentag und Uhrzeit
    :param author: Der author von dem die Commits stammen
    :param filename: in welches File der Plot gespeichert werden soll
    :return: gibt entweder einen Plot als Datei oder als Fernster zurück
    """
    weekdays = []
    hours = []
    sizes = []

    for (weekday, hour), count in commit_counts.items():
        weekdays.append(weekday)
        hours.append(hour)
        sizes.append(count * 50)

    plt.figure(figsize=(10, 6), dpi=100)
    plt.scatter(hours, weekdays, s=sizes, alpha=0.5)

    plt.xlabel('Uhrzeit')
    plt.ylabel('Wochentag')
    plt.title(f'{author}: {sum(commit_counts.values())} commits')

    plt.xlim(-0.5, 24)
    plt.ylim(-0.5, 6.5)
    plt.yticks(ticks=[0, 1, 2, 3, 4, 5, 6], labels=['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'])
    plt.xticks(range(0, 24, 2))

    plt.grid(True)

    if filename:
        plt.savefig(filename)
        print(f"Plot gespeichert als: {filename}")
    else:
        plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="statistik.py by Paul Waldecker -- draws a plot with git log data")

    parser.add_argument('-a', '--author', type=str, default='', help='The author to filter the commits, default=""')
    parser.add_argument('-d', '--directory', type=str, default='.',
                        help='The directory of the git repository, default="."')
    parser.add_argument('-f', '--filename', type=str,
                        help='The filename of the plot. Don\'t save picture if parameter is missing')
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase verbosity')
    parser.add_argument('-q', '--quiet', action='store_true', help='Decrease verbosity')

    args = parser.parse_args()

    verbose = args.verbose and not args.quiet

    if verbose:
        print(f"Git repository: {args.directory}")
        print(f"Author: {args.author}")
        if args.filename:
            print(f"Plot will be saved as: {args.filename}")
        else:
            print("Plot will be displayed.")

    output = run_git_log(args.author, args.directory, verbose)

    if not output:
        print("Keine Commits gefunden.", file=sys.stderr)
        sys.exit(1)

    parsed_commits = parse_git_log(output)
    commit_counts = calculate_commit_counts(parsed_commits)

    create_plot(commit_counts, args.author or "Commits", args.filename)


if __name__ == '__main__':
    main()
