#!/usr/bin/python3

# Import libraries
import re
import bs4
import sys
import time
import progress.bar
import requests
import pyperclip


def main(url, page):
    # Connect to the URL
    response = requests.get(url)
    f = open(page + ".txt", "a+")

    # Parse HTML and save to BeautifulSoup object
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    patron = re.compile(
        r"(http://|https://)[a-z0-9\-\.\/\?=\&]*("
        + page
        + "[.a-z/?#!A-Z0-9-_]*)"
    )

    # To download the whole data set, let's do a for loop through all a tags
    bar1 = progress.bar.Bar("Procesando:", max=len(soup.findAll("a")))
    for i in range(len(soup.findAll("a"))):  # 'a' tags are for links
        one_a_tag = soup.findAll("a")[i]
        try:
            link = one_a_tag["href"]
            if page in link:
                p = patron.match(link)
                urlink = p.group(1) + p.group(2)
                f.write(urlink + "\n")
                pyperclip.copy(urlink)
                pyperclip.paste()
                time.sleep(1)
        except (KeyError):
            pass
        bar1.next()
    bar1.finish()


if __name__ == "__main__":
    # Set the URL you want to webscrape from
    url = sys.argv[1]
    page = sys.argv[2]
    main(url, page)
