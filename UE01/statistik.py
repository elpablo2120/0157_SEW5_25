import argparse

from dateutil import parser
import subprocess
import sys
from collections import defaultdict

from matplotlib import pyplot as plt


def run_git_log(author, path, verbose):
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
    commits = output.split('---END---')
    parsed_commits = []

    for commit in commits:
        if commit.strip():
            author, date = commit.split(';')
            parsed_commits.append({'author': author.strip(), 'date': date.strip()})

    return parsed_commits


def calculate_commit_counts(parsed_commits):
    commit_counts = {}  # Speichert Commit-Anzahl als dict mit (Wochentag, Stunde) als Schlüssel

    for commit in parsed_commits:
        commit_date = parser.parse(commit['date'])
        weekday = commit_date.weekday()  # Wochentag (0 = Montag, 6 = Sonntag)
        hour = commit_date.hour  # Stunde (0-23)
        key = (weekday, hour)

        if key not in commit_counts:
            commit_counts[key] = 0

        commit_counts[key] += 1

    return commit_counts


def create_plot(commit_counts, author, filename=None):
    weekdays = []
    hours = []
    sizes = []

    for (weekday, hour), count in commit_counts.items():
        weekdays.append(weekday)
        hours.append(hour)
        sizes.append(count * 50)  # Größe der Kreise basierend auf Commit-Anzahl

    # Bubble-Plot erstellen
    plt.figure(figsize=(10, 6), dpi=100)
    plt.scatter(hours, weekdays, s=sizes, alpha=0.5)

    # Achsen beschriften
    plt.xlabel('Uhrzeit')
    plt.ylabel('Wochentag')
    plt.title(f'{author}: {sum(commit_counts.values())} commits')

    # Achsenlimits und Beschriftungen anpassen
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

    # Daten parsen und Commit-Anzahl berechnen
    parsed_commits = parse_git_log(output)
    commit_counts = calculate_commit_counts(parsed_commits)

    # Grafik erzeugen
    create_plot(commit_counts, args.author or "Commits", args.filename)


if __name__ == '__main__':
    main()
