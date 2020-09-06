# slid: The Super Lightweight Information Database

This repository is an extension upon a project called [lid](https://github.com/kezz/lid) by [Kieran Wallbanks](https://github.com/kezz).
It is intended for use by Nightlines to create information databases.
Unlike **lid**, this version does not allow users to log onto the website to add and delete entries:
instead, your personal project is meant to be hosted here on GitHub via [GitHub Pages](https://pages.github.com/).
Any changes you make to the information on GitHub, designed to be easy to edit, is mirrored in a matter of minutes on your website.

## Contents

[What is **slid**?](#what-is-slid)

[How does **slid** work?](#how-does-slid-work)

[How do I use **slid**?](#how-do-i-use-slid) (includes full setup instructions)

[FAQ](#faq)

## What is **slid**?

**slid** was developed as [St Andrews Nightline](https://st-andrews.ac.uk/nightline)'s information database,
which contains descriptions and contact details for charities, helplines and University services available to St Andrews students.
It essentially acts as a big phonebook, where each phonebook entry is represented by a coloured card containing a description
and come contact details (e.g. phone, email, website):

IMAGE HERE TO COME

The cards are colour-coded by category and you can filter by category at the top of the page. You can also add "location filters"
which can specify in what parts of the world the content of a particular card is available: for example, if some counselling
services you may be referring to are only available for people in the UK.
There is also a search bar at the top of the page.

If you want to see an example, you can check out what this current repository does at [tomcontileslie.github.io/slid](https://tomcontileslie.github.io/slid).

## How does **slid** work?

**slid** is designed so that the content of the webpage can be edited without any programming knowledge.
Rather than having to edit the HTML source code directly, you edit a set of human-readable files located in the `info/` folder.
Then, when your changes are applied to your copy of this GitHub repository, another program automatically converts the contents
of the information files into machine-readable HTML which is then displayed on your website.

To know what colour each category should be displayed in, the program looks at the file called `style.py` in the `builder/` folder.
The next section will explain how to edit this file if you create a new category or rename a category.

If you wish to add images to some cards, those images must be placed into the `src/img/cards/` folder.

Apart from what's listed above, you should never have to do anything with the other folders in this repository.
The `src/` folder contains the source code for your website, which is what gets updated when you modify the information files.
The `builder/` folder, aside from `style.py`, contains the program which converts your information files into source code.
The `.github/` folder contains instructions telling GitHub to run the card-making program every time you modify the information file.

## How do I use **slid**?

**slid** is free to use. If you re-distribute parts of the code, please include the original MIT license (see the [LICENSE](LICENSE) file).
This is not necessary if you are simply using **slid** to create your own information database, which is what will be explained here.

### 1. Fork this repository
The first step is to make a GitHub account and use it to
[fork this repository](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo).
This will create your personal copy of this project which you are then free to edit so that it contains information relevant
to your specific service.

**Before forking the repo, consider reading [section 4](#4-activate-github-pages-hosting) which may give recommendations about what to name your fork.**

This repository automates lots of things so that you don't have to edit raw HTML at any point. It does this using
[GitHub Actions](https://github.com/features/actions).
When you initially fork the repository, the original Actions are disabled by default. To activate them and set up auto-updates,
go to the "Actions" tab of your fork and confirm that you are happy for the original repository's actions to run.

### 2. Edit the information files
*This step can be repeated at any point, when you wish to update, add, or remove information from your copy of **slid***.

Look inside the `info/` folder. There are currently three sample information files in there:
```
Intro.yml
More Cards.yml
Another Category.yml
```
These just contain demo cards for this repository and you can delete those files,
which will erase the corresponding cards from your copy of **slid**.
You may wish to keep a copy somewhere so you know the template to make new cards.

Each file in the `info/` folder corresponds to a different category:
so although information files can contain multiple cards, all of those cards will have the same colour
on your webpage, and will become grouped together if you filter by that specific category.
To create a new category, perhaps called "Helplines", simply create a new file in the `info/` folder called
`Helplines.yml`. You can then add cards to your file. A card follows this template:
```yml
- title: Samaritans
  image: samaritans_logo.jpg
  content: |
    Whatever you're going through, a Samaritan will face it with you.
    
    The Samaritans phone line is available 24 hours a day, 365 days a year.
  links:
    - text: Website
      url: https://samaritans.org
    - text: 116 123
      url: tel:116123
  locations:
    - England
    - Scotland
    - Ireland
    - Wales
```
In `.yml` files, indentation is very important: so make sure every line, except for the beginning of a new card, starts with two spaces.
Notice how each card starts with a dash, followed by a series of characteristics. A card's characteristics can be some or all of:
```
title:
image:
content:
links:
locations:
```
but if, for example, you don't want to add an image to your card, you can simply remove the line that says `image: file.jpg`.
The same goes for the other characteristics.

There are some details on how to format each characteristic below.

#### `title`
For the `title:` characteristic, enter the title of the card, all on one line.

#### `image`
If you want to add an image, **slid** will put it at the top of the card and draw the title on top.
Pick an image, and add it to the `src/img/cards/` folder.
It's safest to give it a name with no spaces.
Then, write the name of the file you added next to the `image:` characteristic.

#### `content`
The `content:` characteristic can span multiple lines, since you may have a long description to write.
The line with the tag `content:` must look like this:
```
  content: |
```
The vertical bar indicates that the content will be written over multiple lines underneath,
**all indented with four spaces at the start of each line.**
Line breaks in the information files will be translated into HTML line breaks when the cards are built by the program.

#### `links`
Enter as many or as few links as you want in the form of a bulleted list.
Each bullet corresponds to a different link, and must contain a line saying `text:`, as well as a line saying `url:`.
**slid** will display each link with the text you specified; clicking on the link will naviagate the user to the supplied URL.\
For telephone numbers, you can write, e.g.: `url: tel:+441334462266`.

#### `locations`
Just like `links`, the `locations:` characteristic is supplied in the form of a list. Add as many locations as you want.
When building the webpage, **slid** will create a drop-down location filter
which will contain all the locations you have entered in your information files.

### 3. Edit the style file
Every time you add or rename a `.yml` file in the `info/` folder, you have to update the `builder/style.py`
file to let **slid** know what colour each file should be displayed as.
To continue the example from above, suppose you have created a new cateogory in the file `Helplines.yml`,
and you want the Helplines colour to be green. You need to add the following line in the list of colours in `style.py`:
```python
        "Helplines" : "green",
```
make sure that you:
- Have surrounded both the category name and colour name in quotes,
- Have added a comma at the end of the line,
- Have used a colour from the list at the top of the file,
- Have entered the category name so that it is identical to the filename, but with no `.yml` at the end;
- Have inserted your new line after the opening curly bracket, and before the closing one.

### 4. Activate GitHub Pages hosting

Once you have created the content for your website, you are ready to put it online and make it accessible to all.
GitHub offers a website hosting service called [GitHub Pages](https://pages.github.com/) which this repository
is set up to use. While GitHub Pages will do the hosting, you will need to decide on your service's domain name.
Depending on what domain name is available to you, you should read a different sub-section.
We will assume throughout that:

- Your Nightline (or other organisation) is called *Your Nightline* (replace that with your actual name)
- Your Nightline (or other organisation)'s GitHub username is "*@yournightline*".

Now choose one of the following options:

1. Your Nightline has its own website which we will refer to as `https://yournightline.com`,
and you wish your information database to be at a subdomain which we will refer to as
`https://info.yournightline.com`.
In this case, refer to [section 4a](#4a-custom-domain). Note that you must know how to edit your domain's **DNS records**
to carry this out.
2. Your Nightline does not have its own website, or in any case wishes the website to appear at
`https://yournightline.github.io/info`. In this case, refer to [section 4b](#4b-github-page-hosting). You will be able to
customise the `info` part of the link to anything you prefer.
3. Your Nightline wishes the website to appear at `https://yournightline.github.io`. In this case, read
the guidance in [section 4b](#4b-github-page-hosting) and then read what you must do differently in [section 4c](#4c-github-pages-main-website).

#### 4a. Custom domain

Follow the steps below to have your copy of **slid** appear on your own website's subdomain.
We will assume that your fork of **slid** is also called **slid**, though you can replace every
reference to **slid** with your alternate name below if you prefer.

What will effectively happen by carrying out these steps is that you will store your website's
content on your personal GitHub Pages domain: `https://yournightline.github.io/slid`. Then,
you will tell your website to point its subdomain to your GitHub Pages domain to retrieve the
content to display on the page.
This sounds like a redirect,
[but is not the same thing](https://totaluptime.com/kb/whats-the-difference-between-a-cname-and-a-web-redirect/).

We'll assume you're setting up the subdomain `info.yournightline.com`, but you can change `info` to whatever
else you want.

1. **Create a new subdomain with your web hosting provider and update your DNS records.**
On your web hosting provider's control panel, set up a new subdomain called `info.yournightline.com`.
You can also create the corresponding `www` domain, `www.info.yournightline.com`, but this is not compulsory.
Next, update your DNS records. For `info.nightline.com`, add a CNAME record with the text
`yournightline.github.io`. Do the same for the `www` domain if you have one.
2. **Change the CNAME file in slid**. Update the `src/CNAME` file in your fork of **slid** to contain
the address: `info.nightline.com` (don't write `http://` or anything at the start; this holds for the DNS records too).
3. **Activate GitHub Pages hosting**. In your fork of **slid**, go into Settings, and then go to the GitHub Pages section.
As a **Source**, pick the `gh-pages` branch (this branch is automatically updated by GitHub to contain only the contents
of the `src/` folder - so that there aren't any python or YAML files kicking about).
Don't select a theme. Then, enter `info.yournightline.com` as your **Custom domain**.
You can check **Enforce HTTPS**, though whether this works is dependent on your web hosting plan has an SSL
certificate set up.

That should do it! To have all the changes go through, it may be necessary to edit one of the info cards in its
`.yml` file to trigger a full update, which doesn't always happen automatically.

#### 4b. GitHub page hosting

In this section we will assume you want your database to be visible at `https://yournightline.github.io/info`.
You can choose a name other than `info` by replacing all instances of `info` with your preferred name.

1. **Fork the repository**. When you fork the **slid** repository, make sure to name it `info` rather than `slid`.
2. **Delete the CNAME record**. In the `src/` folder, there is a `CNAME` file - only helpful if you are putting the
info database on your own website. Delete it.
3. **Activate GitHub Pages hosting**. In your fork of **slid**, go into Settings, and then go to the GitHub Pages section.
As a **Source**, pick the `gh-pages` branch (this branch is automatically updated by GitHub to contain only the contents
of the `src/` folder - so that there aren't any python or YAML files kicking about).
Don't select a theme.

At this point, your website should be live at the address mentioned above!
To have all the changes go through, it may be necessary to edit one of the info cards in its
`.yml` file to trigger a full update, which doesn't always happen automatically.

#### 4c. GitHub Pages main website

In this section we will assume you want your database to be visible at `https://yournightline.github.io/`, rather
than a subpage like in the previous section.

To do this, follow all the instructions of 4b, but make sure to name your **slid** fork as
`yournightline.github.io`. This will tell GitHub Pages you want **slid** to be your main website homepage,
rather than a subdirectory homepage.

At this point, your website should be live at the address mentioned above!
To have all the changes go through, it may be necessary to edit one of the info cards in its
`.yml` file to trigger a full update, which doesn't always happen automatically.

# FAQ

## All (or some) of my cards are yellow!
The default colour for **slid** cards is yellow, so if **slid** doesn't know what colour to use, it will appear as yellow.
Remember to update the `builder/style.py` file to tell **slid** what colour you want each category to be displayed as.
There are instructions on how to do this above.
Also, make sure that the colour you requested is in the list of colours supplied at the top of the style file, and
you have written the colour name exactly as it is written in that list (all lowercase, with a dash in between words for
colours such as "light-blue", and no spelling mistakes).

## Location filters aren't relevant to my information database. Can I disable the location dropwdown filter?
TBC

## I've just updated the information files but the website hasn't changed!
Start off by giving it a few minutes. When you look at the home page of your repository,
your most recent modification (commit) should appear at the top of the page.
There should be a symbol next to the commit showing the status of the **slid** page build.
Allow a few minutes after the symbol becomes a green tick, for the changes to take effect.
If the symbol becomes a red cross, there is an issue with your modifications.

## The website still hasn't changed, I've been waiting for ages!
By default, if something is wrong with one of your cards in its `.yml` file, **slid** will simply bail and not convert it.
If a card isn't showing up, then you have likely made a syntax mistake when adding its entry in a `.yml` file.
Check that the layout of your information files is exactly the same as the template shown above.
