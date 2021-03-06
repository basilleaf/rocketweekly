import simplejson
import urllib2
from random import randint
from secrets import *
from tumblpy import *

# previously used content is logged to a file, read that file 
published_file = 'published.json'
json_data=open(published_file)
published = simplejson.load(json_data)

# read the json feed for Rocket Launches - see https://scraperwiki.com/scrapers/nasa_grin_rocket_launch_images/
req = urllib2.Request("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=json&name=nasa_grin_rocket_launch_images&query=select+*+from+`swdata`")
opener = urllib2.build_opener()
f = opener.open(req)
data = simplejson.load(f)

# first make sure we haven't already published them all
if len(data) == len(published): 
	published = [] # every post has been published, starting over from scratch

# now remove any previously published posts from data
for k,d in enumerate(data):
    if d['GRIN_id']	in published:
    	del data[k]

# pick a random post from the to-be-published list:
rand = randint(0,len(data)-1)
rocket_launch = data[rand]

# post to tumblr
blog_url = 'rocketweekly.tumblr.com'
t = Tumblpy(app_key = app_key,
        app_secret = app_secret,
        oauth_token = oauth_token,
        oauth_token_secret=oauth_token_secret)
title = rocket_launch['title']
description = rocket_launch['description']
credit = rocket_launch['credit']
link = rocket_launch['page_url']
date = rocket_launch['date']
img_url = rocket_launch['Large']
caption = '<h2>' + title + '</h2><p><b>' + date + '</b></p><p>' + description + '</p>' + credit + '<p>Visit the <a href = "' + link + '">NASA GRIN page</a> for more info and image sizes.'
img = urllib2.urlopen(img_url)
post = t.post('post', blog_url=blog_url, params={'type':'photo', 'caption': caption, 'data': img, 'link':img_url})

# update the published log
if post['id']:
	grin_id = rocket_launch['GRIN_id']
	published.append(grin_id)
	f = open(published_file, 'w')
	simplejson.dump(published, f)
	f.close()

