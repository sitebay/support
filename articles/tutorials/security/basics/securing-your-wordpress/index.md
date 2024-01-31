---
slug: securing-your-wordpress
author:
  name: Site Bay
  email: support@sitebay.org
description: 'This tutorial covers basic best practices for securing a featureion server, including setting up user accounts, configuring a firewall, securing SSH, and disabling unused network services such as XMLRPC.'
og_description: 'This tutorial is a starting point to secure your WordPress Site Bay against unauthorized access, configuring a firewall, securing SSH, and disabling unused network services such as XMLRPC.'
keywords: ["security", "secure", "firewall", "quick start"]
tags: ["wordpress","security"]
license: '[CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0)'
aliases: ['/securing-your-wordpress/']
modified: 2021-08-19
modified_by:
  name: Site Bay
published: 2021-02-17
title: How to Secure Your WordPress
h1_title: Securing Your WordPress
---

In the [Getting Started](/support/getting-started/) tutorial, you learned how to create a site and do basic tasks. Now it's time to secure your site against unauthorized access.

If you want to secure your WordPress site on My Site Bay, one of the best ways to do it is to use our IP-based firewall and HTTP Password Auth features. These tools allow you to control who can access your site and protect it from unauthorized access.

Here's how to use our IP-based firewall and HTTP Password Auth to secure your WordPress site on My Site Bay:

    Log in to My Site Bay with your email and password.

    In the sidebar, navigate to Sites->Your Site-> Tools -> Firewall.

    In the Firewall settings, click on the IP Firewall tab.

    From here, you can add the IP addresses of the devices or networks that you want to allow access to your site.

    Once you have configured your IP firewall, click Save to apply your changes.

    Next, go to the HTTP Password Auth tab and enable HTTP Password Auth for your site.

    The username is always **sitebay** and password will be visible in the tools tab. Now, visitors will need to enter the username and password to view your site.

Now, only users with the correct IP address and password will be able to access your WordPress site on My Site Bay. This added layer of security will help protect your site from unauthorized access and keep your data safe.
