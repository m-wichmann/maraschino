from flask import Flask, jsonify, render_template
import feedparser
import json
import time
import hashlib
import os

from maraschino import logger, app, WEBROOT, DATA_DIR
from maraschino.tools import *
import maraschino
 
DISPLAYED_FEEDS = 5
INCREMENT_FEED = 1

def create_dir(dir):
    if not os.path.exists(dir):
        try:
            logger.log('RSS :: Creating dir %s' % dir, 'INFO')
            os.makedirs(dir)
        except:
            logger.log('RSS :: Problem creating dir %s' % dir, 'ERROR')

create_dir('%s/cache/rss/' % DATA_DIR)


def get_hashed_filename(feed_url):
    return hashlib.md5(feed_url).hexdigest()


def load_cached_feed(feed_url):
    filename = get_hashed_filename(feed_url)
    feed_fd = open(DATA_DIR + '/cache/rss/' + filename + '.json', 'r')
    feed = json.load(feed_fd)
    return feed


def download_and_store_feed(feed_url):
    feed = feedparser.parse(feed_url)
    feed = convert_rss_dates_to_json(feed)

    filename = get_hashed_filename(feed_url)
    feed_fd = open(DATA_DIR + '/cache/rss/' + filename + '.json', 'w')
    json.dump(feed, feed_fd)


def convert_rss_dates_to_json(feed):
    for item in feed["entries"]:
        try:
            item["published_parsed"] = time.asctime(item["published_parsed"])
        except KeyError:
            pass
        try:
            item["updated_parsed"] = time.asctime(item["updated_parsed"])
        except KeyError:
            pass
    try:
        feed["feed"]["updated_parsed"] = time.asctime(feed["feed"]["updated_parsed"])
    except KeyError:
        pass

    return feed

    
@app.route('/xhr/rss_reader/')
@requires_auth
def xhr_rss_reader():

    feed_url = get_setting_value('feed_url')
    feed_fetch_interval = get_setting_value('feed_fetch_interval')

    if feed_fetch_interval == '' or feed_fetch_interval == None:
        feed_fetch_interval = 5


    download_feed = True
    try:
        filename = get_hashed_filename(feed_url)
        json_path = DATA_DIR + '/cache/rss/' + filename + '.json'
        last_feed_download = os.path.getmtime(json_path)
        now = time.time()
        if (now - last_feed_download) < (feed_fetch_interval * 60):
            download_feed = False
    except IOError:
        pass

    if feed_url != None and feed_url != '':
        if download_feed == True:
            print "downloading feed..."
            download_and_store_feed(feed_url)
        print "loading cached feed..."
        feed = load_cached_feed(feed_url)
    else:
        logger.log('Please specify a valid rss feed address.', 'WARNING')
        return render_template('rss_reader.html')
   
    index = 0
    try:
        index_fd = open(DATA_DIR + '/cache/rss/current_index', 'r')
        temp_index = index_fd.readline()
        index = int(temp_index)
    except ValueError:
        pass

    filtered_feeds = []

    feed_entries = feed["entries"]
    feed_count = len(feed["entries"])

    for i in xrange(DISPLAYED_FEEDS):
        entry = feed_entries[(index + i) % feed_count]
        filtered_feeds.append({"title": entry["title"], "link": entry["link"]})

    try:
        index_fd = open(DATA_DIR + '/cache/rss/current_index', 'w')
        index_fd.write(str((index + INCREMENT_FEED) % feed_count))
    except IOError:
        pass



    feed_title0 = filtered_feeds[0]["title"]
    feed_url0 = filtered_feeds[0]["link"]
    feed_title1 = filtered_feeds[1]["title"]
    feed_url1 = filtered_feeds[1]["link"]
    feed_title2 = filtered_feeds[2]["title"]
    feed_url2 = filtered_feeds[2]["link"]
    feed_title3 = filtered_feeds[3]["title"]
    feed_url3 = filtered_feeds[3]["link"]
    feed_title4 = filtered_feeds[4]["title"]
    feed_url4 = filtered_feeds[4]["link"]

    return render_template('rss_reader.html',
        feed_title0 = feed_title0,
        feed_url0 = feed_url0,
        feed_title1 = feed_title1,
        feed_url1 = feed_url1,
        feed_title2 = feed_title2,
        feed_url2 = feed_url2,
        feed_title3 = feed_title3,
        feed_url3 = feed_url3,
        feed_title4 = feed_title4,
        feed_url4 = feed_url4,
    )














