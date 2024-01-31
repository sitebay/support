---
slug: how-git-sync-works-with-point-in-time-machine
author:
  name: Site Bay Community
  email: support@sitebay.org
description: 'Learn how Site Bay''s Point-in-Time Machine interacts with Git Sync'
keywords: ['git-sync', 'pit-machine']
license: '[CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0)'
published: 2019-03-26
modified: 2019-03-26
modified_by:
  name: Site Bay
title: "How Git Sync Works With PIT Machine"
h1_title: "Restoring your Git Sync Enabled Site"
contributor:
  name: Site Bay
tags: ["sitebay platform","development", "git sync"]
aliases: ['/platform/git-sync/how-git-sync-works-with-point-in-time-machine/']
---

![How to Use Site Bay's Git Sync](how-git-sync-works-with-point-in-time-machine.png "How to Use Site Bay's Git Sync")

Do you have a WordPress site set up with our Bi-Directional Git Sync? It also works with our Point-in-Time machine to restore your database and files to any point, down to the minute.


## How We Restore Your WordPress Files

When you restore your Git Sync Enabled WordPress site Using the PIT Machine from My Site Bay, the **git revert** command is run on your repo. 
The revert command creates a commit with the reverse patch to cancel it out. This way,  no history is overwritten. If you decide you didn't want to restore after, you can use the PIT machine to go back to the point just before you did the initial restore.

When you restore your site to a time in Site Bay's PIT Machine, we will find the commit hash for your repo at that point. 
Then, we revert everything from the HEAD commit (the state of your current site's repo) back to the restore's commit hash, meaning it will recreate that commit state in the tree. This would be like if every commit after your selected restore point had been walked back to the repo state at the restore point. We then commit the current tree, and it will create a brand new commit equivalent to the commit you restored. This way, you don't have to worry about losing data from any point-in-time.

{{< note >}}
We recommend using the Point-in-Time Machine for restoring your site. If you try to issue git revert commands from your local repo, your database will not be restored and your content folder and database may be incompatible with eachother.
{{< /note >}}