---
title: "{{ replace .TranslationBaseName "-" " " | title }}"
description: 'Two to three sentences describing your tutorial.'
keywords: []
license: '[CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0)'
authors: ["Site Bay"]
published: {{ now.Format "2006-01-02" }}
modified: {{ now.Format "2006-01-02" }}
modified_by:
  name: Site Bay
headless: true
show_on_rss_feed: false
---

<!--- Describe the shorttutorial, including any choices made (e.g. installs Python using Miniconda, only works for Debian and Ubuntu, etc. -->

1.  Step 1

2.  Step 2

3.  Step 3
