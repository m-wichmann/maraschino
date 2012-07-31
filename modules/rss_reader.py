from flask import Flask, jsonify, render_template
import feedparser
import json
import time
import hashlib

from maraschino import logger, app, WEBROOT, DATA_DIR
from maraschino.tools import *
import maraschino
 

def create_dir(dir):
    if not os.path.exists(dir):
        try:
            logger.log('RSS :: Creating dir %s' % dir, 'INFO')
            os.makedirs(dir)
        except:
            logger.log('RSS :: Problem creating dir %s' % dir, 'ERROR')

create_dir('%s/cache/rss/' % DATA_DIR)


def load_cached_feed(feed_url):
    filename = hashlib.md5(feed_url).hexdigest()
    feed_fd = open(DATA_DIR + '/cache/rss/' + filename + '.json', 'r')
    feed = json.load(feed_fd)
    return feed


def download_and_store_feed(feed_url):
    feed = feedparser.parse(feed_url)
    feed = convert_rss_dates_to_json(feed)

    filename = hashlib.md5(feed_url).hexdigest()
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

    
@app.route('/xhr/rss_reader')
@requires_auth
def xhr_rss_reader():

    feed_url = get_setting_value('feed_url')

    download_and_store_feed(feed_url)
    feed = load_cached_feed(feed_url)

    feed_title0 = feed["entries"][0]["title"]
    feed_url0 = feed["entries"][0]["link"]
    feed_title1 = feed["entries"][1]["title"]
    feed_url1 = feed["entries"][1]["link"]
    feed_title2 = feed["entries"][2]["title"]
    feed_url2 = feed["entries"][2]["link"]
    feed_title3 = feed["entries"][3]["title"]
    feed_url3 = feed["entries"][3]["link"]
    feed_title4 = feed["entries"][4]["title"]
    feed_url4 = feed["entries"][4]["link"]

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














