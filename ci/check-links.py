#!/usr/bin/env python
import os
import sys
import re
import frontmatter
import textwrap
import argparse

# Define command-line arguements
parser = argparse.ArgumentParser(description="Check links within Markdown.")
parser.add_argument(
    "--fix_issues",
    help="Attempts to fix some types of issues.",
    default=False,
    action=argparse.BooleanOptionalAction,
)
ARGS = parser.parse_args()

# Identifies if --fix_issues arguement has been used and, if so, set FIX_ISSUES to true
FIX_ISSUES = False
if ARGS.fix_issues:
    FIX_ISSUES = True


class Tutorial:
    def __init__(self, root, path, title, link):
        self.root = root
        self.path = path
        self.title = title
        self.link = link
        self.aliases = []
        self.assets = []
        self.anchors = []
        self.issues = []
        self.logged = False

    def add_aliases(self, aliases):
        self.aliases = aliases

    def add_asset(self, asset):
        self.assets.append(asset)

    def add_anchor(self, anchor):
        self.anchors.append(anchor)

    def add_issue(self, issue):
        self.issues.append(issue)

    def log_tutorial(self):
        self.logged = True


class Asset:
    def __init__(self, path, link):
        self.path = path
        self.link = link


class Alias:
    def __init__(self, link, tutorial):
        self.link = link
        self.tutorial = tutorial


class Issue:
    def __init__(self, link, type_id):
        self.link = link
        self.type_id = type_id
        self.affected_tutorials = []
        self.notes = ""

    def add_tutorial(self, tutorial):
        self.affected_tutorials.append(tutorial)

    def add_notes(self, notes):
        self.notes = notes


class IssueType:
    def __init__(self, id, title, summary, severity, weight):
        self.id = id
        self.title = title
        self.summary = summary
        self.severity = severity
        self.weight = weight
        self.num_issues = 0
        self.issues = []

    def set_num_issues(self, count):
        self.num_issues = count

    def add_issue(self, issue):
        self.issues.append(issue)


DOCS_DIR = [
    "docs/tutorials",
    "docs/features",
    "docs/bundles",
    "docs/assets",
    "docs/api",
    "docs/reference-architecture",
    "docs/release-notes",
]

# Create all issue types
issue_types = []
issue_types.append(
    IssueType(
        id="not-found",
        title="Target not found",
        summary="The link's target has not been found (would likely result in a 404 error).",
        severity="failure",
        weight=0,
    )
)
issue_types.append(
    IssueType(
        id="duplicate-alias",
        title="Duplicate alias",
        summary="This alias appears in multiple tutorials.",
        severity="failure",
        weight=10,
    )
)
issue_types.append(
    IssueType(
        id="slug-mismatch",
        title="Slug mismatch",
        summary="The tutorial's slug does not match the name of its parent folder.",
        severity="failure",
        weight=15,
    )
)
issue_types.append(
    IssueType(
        id="docs-domain-name",
        title="Contains domain name",
        summary="The link contains the domain name of the docs site.",
        severity="failure",
        weight=20,
    )
)
issue_types.append(
    IssueType(
        id="incorrect-root",
        title="Incorrect root directory",
        summary="The link does not point to the correct root (/support/)",
        severity="failure",
        weight=30,
    )
)
issue_types.append(
    IssueType(
        id="other",
        title="Other issues",
        summary="The link contains other unspecified issues, like extra characters or incorrect formatting.",
        severity="failure",
        weight=40,
    )
)
issue_types.append(
    IssueType(
        id="points-to-alias",
        title="Target is alias",
        summary="The link points to an alias of tutorial instead of its current URL.",
        severity="warning",
        weight=50,
    )
)


# ------------------
# Build a list of all tutorials
# ------------------
def get_tutorials():
    tutorials = []
    assets = []
    issues = []

    # Add top level tutorials
    tutorials.append(Tutorial("docs/", "docs/_index.md", "Docs Home", "/support/"))
    tutorials.append(
        Tutorial(
            "docs/features/",
            "docs/features/_index.md",
            "Product Docs",
            "/support/features/",
        )
    )
    tutorials.append(
        Tutorial("docs/marketplace/", "", "Marketplace", "/support/marketplace/")
    )
    tutorials.append(
        Tutorial("docs/resources/", "", "Resources", "/support/resources/")
    )
    tutorials.append(
        Tutorial(
            "docs/topresults/?docType=community",
            "",
            "Q&A",
            "/support/topresults/?docType=community",
        )
    )
    assets.append(Asset("/support/api/openapi.yaml", "/support/api/openapi.yaml"))

    # Iterate through each file in each docs directory
    for dir in DOCS_DIR:
        for root, dirs, files in os.walk(dir):
            for file in files:
                # The relative file path of the file
                file_path = os.path.join(root, file)
                path_segments = file_path.split("/")

                # If the file is markdown..
                if file.endswith(".md"):
                    try:
                        # Loads the entire tutorial (including front matter)
                        expanded_tutorial = frontmatter.load(file_path)

                        # Ignores the tutorial if it's headless
                        if "headless" in expanded_tutorial.keys():
                            if expanded_tutorial["headless"] == True:
                                continue

                        # Identifies the canonical link for a tutorial
                        # ... If the tutorial is in the tutorials section...
                        if (
                            "slug" in expanded_tutorial.keys()
                            and "docs/tutorials/" in file_path
                        ):
                            # If the slug does not match the parent folder, log issue
                            if not expanded_tutorial["slug"] == path_segments[-2]:
                                issues.append(
                                    Issue(expanded_tutorial["slug"], "slug-mismatch")
                                )

                                # Attempt to fix this issue
                                if FIX_ISSUES == True:
                                    path_segments[-1] = ""
                                    old_file_path = "/".join(path_segments)
                                    path_segments[-2] = expanded_tutorial["slug"]
                                    new_file_path = "/".join(path_segments)
                                    # print("Old file path: " + old_file_path)
                                    # print("New file path: " + new_file_path)
                                    os.rename(old_file_path, new_file_path)

                            canonical_link = (
                                "/support/tutorials/" + expanded_tutorial["slug"] + "/"
                            )
                        # ... If the tutorial is in the API section...
                        elif (
                            "slug" in expanded_tutorial.keys()
                            and "docs/api/" in file_path
                        ):
                            canonical_link = (
                                "/support/api/" + expanded_tutorial["slug"] + "/"
                            )
                        # ... If the tutorial is in any other section...
                        else:
                            canonical_link = "/" + file_path
                            canonical_link = canonical_link.replace("/index.md", "/")
                            canonical_link = canonical_link.replace("/_index.md", "/")

                        # Construct the tutorial object
                        tutorial = Tutorial(
                            root, file_path, expanded_tutorial["title"], canonical_link
                        )

                        # Add aliases to the tutorial object if they exist
                        if "aliases" in expanded_tutorial.keys():
                            tutorial.add_aliases(expanded_tutorial["aliases"])

                        # Find assets
                        if file == "index.md":
                            tutorial = get_tutorial_assets(tutorial)

                        # Append the tutorial object to the list of tutorials
                        tutorials.append(tutorial)

                    except Exception as e:
                        print(e)

                # If the file is something else, like an image or other asset...
                else:
                    if "docs/tutorials/" in file_path:
                        link = (
                            "/support/tutorials/"
                            + path_segments[-2]
                            + "/"
                            + path_segments[-1]
                        )
                    else:
                        link = "/" + file_path
                    assets.append(Asset(file_path, link))

    return tutorials, assets, issues


# ------------------
# Get tutorial assets
# ------------------
def get_tutorial_assets(tutorial):
    # Walk through all files within the tutorial's directory
    for root, dirs, files in os.walk(tutorial.root):
        for file in files:
            # If the file is index.md, skip it
            if file == "index.md":
                continue

            # Build the full path to the file
            path = os.path.join(root, file)

            # Build the relative link to the file
            relative_link = path.replace(tutorial.root, "")

            # If the relative link starts with a slash, remove it
            if relative_link.startswith("/"):
                relative_link = relative_link.lstrip("/")

            # Add the file as an asset to the tutorial
            tutorial.assets.append(Asset(path, relative_link))
    return tutorial


# ------------------
# Check for duplicate aliases
# ------------------
def get_duplicate_aliases(tutorials):
    aliases = set()
    issues = []

    for tutorial in tutorials:
        for alias in tutorial.aliases:
            if alias in aliases:
                issues.append(Issue(alias, "duplicate-alias"))
            else:
                aliases.add(alias)

    return issues


# ------------------
# Check internal links
# ------------------
def check_internal_links_markdown(tutorials, assets):
    # The regex pattern used to locate all markdown links containing the string "/docs".
    # This bypasses any external urls and archor links
    link_pattern = re.compile("(?:[^\!]|^)\[([^\[\]]+)\]\(()([^()]+)\)")

    # Array of special elements to ignore
    starting_elements_to_ignore = [
        "```",
        "{{< file",
        "{{<file",
        "{{< command",
        "{{<command",
        "{{< output",
        "{{<output",
    ]
    ending_elements_to_ignore = [
        "```",
        "{{</file",
        "{{</ file",
        "{{< /file",
        "{{</command",
        "{{</ command",
        "{{< /command",
        "{{</output",
        "{{</ output",
        "{{< /output",
    ]

    list_elements = ["-", "*", "."]

    issues = []

    for tutorial in tutorials:
        # Ignore tutorials with no file path
        if tutorial.path == "":
            continue

        expanded_tutorial = frontmatter.load(tutorial.path)

        # Reset insideSpecialElement for each new file
        insideSpecialElement = False

        # Build a list of each line in a file
        lines = open(tutorial.path)

        previous_indent = 0
        previous_line = ""

        # Iterate through each line of the file
        for i, line in enumerate(lines):
            # Ignore certain code elements
            if line.lstrip().startswith(tuple(starting_elements_to_ignore)):
                insideSpecialElement = True
                continue
            elif line.lstrip().startswith(tuple(ending_elements_to_ignore)):
                insideSpecialElement = False
                continue
            if insideSpecialElement == True:
                continue

            # Set the current indent
            current_indent = len(line) - len(line.lstrip())

            # Strip out any numbers at the start of the line
            line = re.sub("^\d+", "", line)

            # Ignore indented code blocks (recognizing the difference between indents for lists and indents for code blocks)
            if (
                previous_line.lstrip().startswith(tuple(list_elements))
                and (current_indent - previous_indent) >= 6
            ):
                continue
            elif (
                not previous_line.lstrip().startswith(tuple(list_elements))
                and (current_indent - previous_indent) >= 3
            ):
                continue
            # Set the previous indent if not in an indented code block
            else:
                previous_indent = current_indent
                previous_line = line

            # Remove all inline code blocks from the line
            line = re.sub(r"(?<!\\)(`.*?(?<!\\)`)", "", line)

            # Find and iterate through all markdown links
            for match in re.finditer(link_pattern, line):
                # Remove the title, brackets, and parenthesis from the markdown link syntax
                link = match.group(3)
                link_unmodified = link

                # Log issue if link contains "sitebay.org/support/"
                if "sitebay.org/support/" in link:
                    issues.append(Issue(link_unmodified, "docs-domain-name"))
                    continue
                # Ignore links that start with common protocols
                if (
                    link.startswith("http://")
                    or link.startswith("https://")
                    or link.startswith("ftp://")
                ):
                    continue
                # Check if link points to an asset link
                if next((x for x in assets if x.link == link), None):
                    continue
                # Check if links point to an asset within its own directory
                if next((x for x in assets if x.link == tutorial.link + link), None):
                    continue
                # Check if links point to the relative link of an asset
                if next((x for x in tutorial.assets if x.link == link), None):
                    continue
                # Ignore anchors
                if link.startswith("#"):
                    continue
                elif "#" in link:
                    link = link.split("#", 1)[0]
                # Ignore links to resources within the same directory
                if not "/" in link and "." in link:
                    continue
                # Log issue if link does not start with /support/
                if not link.startswith("/support/"):
                    issues.append(Issue(link_unmodified, "incorrect-root"))
                    continue
                # Log issue if link ends with two slashes /
                if "//" in link:
                    # Log issue if link ends with two slashes /
                    issues.append(Issue(link_unmodified, "formatting"))
                    link = link.replace("//", "/")
                if not link.endswith("/"):
                    # Log warning if link does not end with a slash /
                    issues.append(Issue(link_unmodified, "formatting"))
                    link = link + "/"
                # Check if link points to a canonical internal link
                if not next((x for x in tutorials if x.link == link), None):
                    # Checks if the link matches an alias or not
                    if (
                        next(
                            (
                                x
                                for x in tutorials
                                if link.replace("/support/", "/") in x.aliases
                            ),
                            None,
                        )
                        is not None
                    ):
                        issues.append(Issue(link_unmodified, "points-to-alias"))
                    else:
                        issues.append(Issue(link_unmodified, "not-found"))

    return issues


# ------------------
# Main function
# ------------------
def main():
    test_failed = False
    issues = []
    tutorials, assets, issues = get_tutorials()

    issues = issues + (get_duplicate_aliases(tutorials))
    issues = issues + (check_internal_links_markdown(tutorials, assets))

    # Iterate through each issue type. Then, iterate through all issues
    # and add issues belonging to the specified issue type.
    for t in issue_types:
        for i in issues:
            if i.type_id == t.id:
                t.add_issue(i)

    # Sorts the issue type based on the weight
    issue_types.sort(key=lambda x: x.weight)

    # Check if there are any failures. If so, set test_failed to true
    for t in issue_types:
        if t.severity == "failure" and not len(t.issues) == 0:
            test_failed = True
            break

    # Output Summary
    print(
        textwrap.dedent(
            f"""
    {'='*40}

    MARKDOWN LINK TESTER

    This test analyzes the markdown links within our library.
    Valid external links (links pointing to other sites) are ignored.
    Otherwise, if the link is not valid or does not point to a
    tutorial or asset on the docs site, an issue is logged.

    Number of tutorials: {str(len(tutorials))} (with {str(len(assets))} assets)
    """
        )
    )

    for t in issue_types:
        print(f"    {t.title} ({(t.severity).upper()}): {str(len(t.issues))}")

    # Output the result of the test. If the test has failed, return a
    # failure to GitHub Actions.
    if not test_failed:
        print(
            textwrap.dedent(
                f"""
        TEST SUCCEEDED!

        {'='*40}
        """
            )
        )
    else:
        print(
            textwrap.dedent(
                f"""
        TEST FAILED!

        {'='*40}
        """
            )
        )

        # Output information about each issue type and any associated issues
        for t in issue_types:
            if t.severity == "failure" and not len(t.issues) == 0:
                # Output heading for this issue type
                print(
                    textwrap.dedent(
                        f"""
              {t.title} ({(t.severity).upper()}): {str(len(t.issues))}
                  {t.summary}
              """
                    )
                )
                # Output the list of errors if the issue severity is a failure
                for i in t.issues:
                    print(f"    - {i.link}")

        sys.exit(1)


if __name__ == "__main__":
    main()
