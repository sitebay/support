from tabulate import tabulate
from operator import itemgetter
import frontmatter
import sys
import glob


def make_record(yaml):
    """Create a dictionary object from yaml front matter"""

    if "title" in yaml:
        title = yaml["title"]
    else:
        title = "No title"
    record = {"title": title, "updated": yaml["modified"]}
    return record


def find_old_tutorials(count=20):
    """Print a list of the 20 oldest tutorials in the library.

    Results are sorted by modification date (in front matter)
    and deprecated tutorials are ignored.

    Command line arguments:
    count: number of tutorials to list (default: 20)
    """
    old_tutorials = []
    tutorials_scanned = 0
    rootdir = "docs"
    for filename in glob.glob("docs/**/*.md", recursive=True):
        tutorials_scanned += 1
        with open(filename, "r") as f:
            yaml = frontmatter.loads(f.read())
            if "modified" in yaml and "deprecated" not in yaml:
                record = make_record(parsed)
                record["path"] = filename
                old_tutorials.append(record)
    print(str(tutorials_scanned) + " tutorials scanned.")
    old_tutorials.sort(key=itemgetter("updated"))
    oldest_tutorials = old_tutorials[0:count]
    print(tabulate(oldest_tutorials))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        count = int(sys.argv[1])
    else:
        count = 20
    find_old_tutorials(count)
