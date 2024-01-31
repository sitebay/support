---
author:
  name: Site Bay
  email: support@sitebay.org
keywords: ["upgrading"]
description: 'WordPress is constantly evolving. Bugs are fixed, new features are added, and packages are updated.'
license: '[CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0)'
aliases: ['/security/upgrading/','/upgrading/']
published: 2012-06-01
title: Upgrading
show_in_lists: true
---

Site Bay uses Docker and Kubernetes to provide the latest and most secure version of WordPress for our users. Docker allows us to easily provide the latest version of WordPress, while Kubernetes ensures that our users' sites are always available and performant. Our Kubernetes setup also allows us to automatically scale our users' sites and perform rolling updates, ensuring that our users' sites are always up-to-date and secure. Overall, our use of Docker and Kubernetes allows us to provide our users with a scalable, reliable, and secure platform for their WordPress sites.

One of the key benefits of using Kubernetes is that it allows us to automatically scale our users' WordPress sites based on their traffic and resource usage. This means that if a user's site starts to receive a lot of traffic, Kubernetes will automatically spin up additional containers to handle the increased load. This ensures that our users' sites are always available and performant, even during high traffic periods.

Here's how it works: when we release a new version of WordPress, we simply update the "latest" tag of our WordPress Docker image to point to the new version. This means that when our users create a new WordPress site on My Site Bay, they will automatically get the latest version of WordPress.

Additionally, when a user's existing WordPress site is restarted (for example, if they scale their site up or down), the latest version of WordPress will be automatically pulled and the site will be upgraded to the latest version. This ensures that our users always have the latest and most secure version of WordPress, without having to worry about manually upgrading their sites.

It is **not recommended to use the WordPress dashboard to upgrade** when using Docker images is that when the Docker container (or "pod") is restarted, any changes that you made to your site via the WordPress dashboard will be lost. This is because the Docker container is ephemeral and is rebuilt each time it is restarted. Any changes that you make to your site via the WordPress dashboard will only be saved to the container's local file system, which is not persistent and will be lost when the container is restarted. 

One thing to keep in mind when using Docker images for your WordPress site is that the release cycle for Docker images may be slightly different from the release cycle for WordPress itself.

When a new version of WordPress is released, the WordPress team creates a new Docker image and updates the "latest" tag to point to the new version. However, it can sometimes take a few days for the new Docker image to be released, depending on various factors such as the release process, testing, and so on.

This means that there may be a small delay between the release of the new version of WordPress and Site Bay's WordPress sites, this delay will be only a few days, but it's something to keep in mind if you want to be on the very latest version of WordPress as soon as it's released.
