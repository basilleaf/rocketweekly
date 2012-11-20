import simplejson
import urllib2
import tumblpy
from random import randint

# previously used content is logged to a file, read that file 
published_file = 'published.json'
json_data=open(published_file)
published = simplejson.load(json_data)

# read the json feed for Rocket Launches - see https://scraperwiki.com/scrapers/nasa_grin_rocket_launch_images/
req = urllib2.Request("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=json&name=nasa_grin_rocket_launch_images&query=select+*+from+`swdata`")
opener = urllib2.build_opener()
f = opener.open(req)
data = simplejson.load(f)

# first checking that we haven't already published them all
if len(data) == len(published): 
	published = [] # every post has been published, starting over from scratch

# now remove any previously published posts from data
for k,d in enumerate(data):
    if d['GRIN_id']	in published:
    	del data[k]

# then pick a random one:
rand = randint(0,len(data)-1)
rocket_launch = data[rand]

# update the published log
grin_id = rocket_launch['GRIN_id']
published += [grin_id]
f = open(published_file, 'w')
simplejson.dump(published, f)
f.close()

# and tumblr post it
# tumblr suspended me wtf.. todo.. something like:
t = Tumblpy(app_key = '*your app key*',
        app_secret = '*your app secret*',
        oauth_token=oauth_token,
        oauth_token_secret=oauth_token_secret)

blog_url = "BLOG URL"
post = rocket_launch['title'] + '<br>' + rocket_launch['description']
img = urllib2.urlopen(rocket_launch['Large']).read()
post = t.post('post', blog_url=blog_url, params={'type':'photo', 'caption': post, 'data': img})
print post  # returns id if posted successfully
