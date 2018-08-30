#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup


def get_soup(url, num_retries=10):
    """
    Takes in a url and returns the parsed BeautifulSoup code for that url with
    handling capabilities if the request 'bounces'.
    """

    s = requests.Session()

    retries = Retry(
        total=num_retries,
        backoff_factor=0.1,
        status_forcelist=[500, 502, 503, 504]
    )

    s.mount('http://', HTTPAdapter(max_retries=retries))

    return BeautifulSoup(s.get(url).text, 'html.parser')


def get_item_number(soup):
    """
    Returns the product's unique item_number
    """

    item_number = soup.find('div', attrs={'id': 'descItemNumber'})

    if not item_number:
        return "N/A"

    item_number = item_number.get_text()

    return item_number


def get_title(soup):
    """
    Returns the product title. If there is an unknown character in the title, it
    returns it as '?'.
    """

    title = soup.find('h1', attrs={'class': 'it-ttl'})

    if not title:
        return "N/A"

    for i in title('span'):
        i.extract()
    title = title.get_text()  # .encode('ascii', 'replace')

    return title


def get_current_price(soup):
    """
    Returns the product's current price
    """
    now_price = soup.find('span', attrs={'id': 'mm-saleDscPrc'})
    if not now_price:
        return "N/A"
    return now_price.get_text()


def get_item_specific(soup):
    """
    Returns a dictionary containing the item information.
    """
    item_description = soup.find('div', attrs={'id': 'viTabs_0_is'})
    table = item_description.find_all('table')[-1]
    labels = table.find_all('td', attrs={'class': 'attrLabels'})  # text="Size (Women's):")

    size = labels[-3].findNext('td').get_text() or 'N/A'
    color = table.find('h2', attrs={'itemprop': 'color'}).get_text() or 'N/A'

    return dict(size=size.replace('\n', ''), color=color)


def scrape_product_info(url, num_retries=10):
    """
    from app_scraper.utils.scraper import scrape_product_info
    scrape_product_info('https://www.ebay.com/itm/273402419771?hash=item3fa80dda3b:g:F9EAAOSwkRha0PHk')
    scrape_product_info('https://www.ebay.com/itm/Bill-Blass-Womens-Short-Sleeve-Button-Front-Blouse-Sz-M-White-/273381497394')

    {'item_specific': {'color': 'Black', 'size': 'S'},
     'current_price': 'US $13.99',
     'item_id': '273402419771',
     'name': b"Baju Women's Sleeveless Maxi Dress w/ Pockets Sz. S Black White Turle Print"
     }

    {'name': b"Bill Blass Women's Short Sleeve Button Front Blouse Sz. M White",
     'current_price': 'US $6.99',
     'item_id': '273381497394',
     'item_specific': {'color': 'White', 'size': 'Regular'}
     }
    """
    soup = get_soup(url, num_retries)

    product_dict = {
        'item_id': get_item_number(soup),
        'name': get_title(soup),
        'current_price': get_current_price(soup),
        'item_specific': get_item_specific(soup),
    }
    return product_dict
