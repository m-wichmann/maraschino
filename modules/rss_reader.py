# -*- coding: utf-8 -*-
"""RSS feed reader module for Maraschino"""

from flask import render_template
import feedparser
import time
import hashlib
import urllib
import os

from maraschino import logger, DATA_DIR
from maraschino.tools import *
import maraschino
 
DISPLAYED_FEEDS = 5
INCREMENT_FEED = 1

def create_dir(target_dir):
    """create rss feed cache dir"""
    if not os.path.exists(target_dir):
        try:
            logger.log('RSS :: Creating dir %s' % target_dir, 'INFO')
            os.makedirs(target_dir)
        except OSError:
            logger.log('RSS :: Problem creating dir %s' % target_dir, 'ERROR')

# TODO: use os.sep
create_dir('%s/cache/rss/' % DATA_DIR)

def get_hashed_filename(feed_url):
    """return a hashed filename for a given feed url"""
    hashed_url = hashlib.md5(feed_url)
    return hashed_url.hexdigest()

def load_cached_feed(feed_url):
    """load cached xml feed for given url"""
    filename = get_hashed_filename(feed_url)
    # TODO: use os.sep
    filepath = DATA_DIR + '/cache/rss/' + filename + '.xml'
    feed = feedparser.parse(filepath)
    return feed

def download_and_store_feed(feed_url):
    """download feed xml from url"""
    # get feed xml from url
    try:
        feed_xml = urllib.urlopen(feed_url)
        # open local file
        filename = get_hashed_filename(feed_url)
        feed_fd = open(DATA_DIR + '/cache/rss/' + filename + '.xml', 'w')    

        # download feed xml
        feed_fd.write(feed_xml.read())
        feed_xml.close()
        feed_fd.close()
    except IOError:
        return -1
    
@app.route('/xhr/rss_reader/')
@requires_auth
def xhr_rss_reader():
    """Main rss reader module function"""
    # get settings from maraschino
    feed_url = get_setting_value('feed_url')
    feed_fetch_interval = get_setting_value('feed_fetch_interval')

    # if no interval is set use the default
    if feed_fetch_interval == '' or feed_fetch_interval == None:
        feed_fetch_interval = 5

    # if a valid feed url is present
    try:
        if feed_url == None or feed_url == '':
            raise ValueError
        # check if the feed should be downloaded (is to old)
        download_feed = True
        try:
            # build file name/path
            filename = get_hashed_filename(feed_url)
            # TODO: use os.sep
            xml_path = DATA_DIR + '/cache/rss/' + filename + '.xml'
            # get last modified time
            last_feed_download = os.path.getmtime(xml_path)
            now = time.time()
            # check if calculated time is below interval
            if (now - last_feed_download) < (feed_fetch_interval * 60):
                download_feed = False
        except OSError:
            pass
        except IOError:
            pass

        if download_feed == True:
            # download and store feed locally
            ret = download_and_store_feed(feed_url)
            if ret == -1:
                raise ValueError
        # load feed from local cache
        feed = load_cached_feed(feed_url)
    except ValueError:
        logger.log('Please specify a valid rss feed address.', 'WARNING')
        return render_template('rss_reader.html',
            valid_feed = False
        )

    # get current feed index for rotation
    index = 0
    try:
        index_fd = open(DATA_DIR + '/cache/rss/current_index', 'r')
        temp_index = index_fd.readline()
        index = int(temp_index)
    except IOError:
        pass
    except ValueError:
        pass

    filtered_feeds = []

    feed_entries = feed["entries"]
    feed_count = len(feed["entries"])

    # filter feeds according to rotation index and displayed feed count
    for i in xrange(DISPLAYED_FEEDS):
        entry = feed_entries[(index + i) % feed_count]
        filtered_feeds.append({"title": entry["title"], "link": entry["link"]})

    # write back new index
    try:
        index_fd = open(DATA_DIR + '/cache/rss/current_index', 'w')
        index_fd.write(str((index + INCREMENT_FEED) % feed_count))
    except IOError:
        pass

    # set feedtitle
    feedtitle = "RSS Feed: " + feed["feed"]["title"]

    # render the template...
    return render_template('rss_reader.html',
        valid_feed = True,
        feedtitle = feedtitle,
        feeditems = filtered_feeds
    )
