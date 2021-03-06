# -*- coding:utf-8 -*- #
#! /usr/bin/env python

import time
import cPickle as pickle
#sys.path.insert(0, 'tweibo.zip')
from tweibo import *
import ConfigParser
import os
import sched

config = ConfigParser.ConfigParser()
config.read('config.ini')
# 换成你的 APPKEY
APP_KEY = config.get('APPKEY', 'appkey')
APP_SECRET = config.get('APPKEY', 'appsecret')
CALLBACK_URL = "https://github.com"
# 请先按照 https://github.com/upbit/tweibo-pysdk/wiki/OAuth2Handler 的鉴权说明填写 ACCESS_TOKEN 和 OPENID
ACCESS_TOKEN = config.get('APPKEY', 'access_token')
OPENID = config.get('APPKEY', 'openid')
OPENKEY = config.get('APPKEY', 'openkey')
IMG_EXAMPLE = "example.png"

# 返回text是unicode，设置默认编码为utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def access_token_test():
    """ 访问get_access_token_url()的URL并授权后，会跳转callback页面，其中包含如下参数：
        #access_token=00000000000ACCESSTOKEN0000000000&expires_in=8035200&openid=0000000000000OPENID0000000000000&openkey=0000000000000OPENKEY000000000000&refresh_token=0000000000REFRESHTOKEN00000000&state=
    保存下其中的 access_token, openid 并调用
        oauth.set_access_token(access_token)
        oauth.set_openid(openid)
    即可完成 OAuth2Handler() 的初始化。可以记录 access_token 等信息
    """
    oauth = OAuth2Handler()
    oauth.set_app_key_secret(APP_KEY, APP_SECRET, CALLBACK_URL)
    print oauth.get_access_token_url()

def checkdir(path):
    if os.path.exists(path) == 0:
        os.mkdir(path)


def gettimelie(api, name):
    user_timeline = api.get.statuses__user_timeline(format="json", name=name,
            reqnum=100, pageflag=0, lastid=0, pagetime=0, type=3, contenttype=0)
    for idx, tweet in enumerate(user_timeline.data.info):
        checkdir('weibo/' + tweet.name)
        f1 = file('weibo/' + tweet.name + '/' + tweet.id + '.pkl','wb')
        pickle.dump(tweet, f1, True)

def tweibo_api():
    oauth = OAuth2Handler()
    oauth.set_app_key_secret(APP_KEY, APP_SECRET, CALLBACK_URL)
    oauth.set_access_token(ACCESS_TOKEN)
    oauth.set_openid(OPENID, OPENKEY)
    api = API(oauth)
    return api




def tweibo_test():
    api = tweibo_api()
    #userlist = open('weibo/list', 'w')
    #api = API(oauth, host="127.0.0.1", port=8888)       # Init API() with proxy

    # GET /t/show
    #tweet1 = api.get.t__show(format="json", id=301041004850688)
    #print ">> %s: %s" % (tweet1.data.nick, tweet1.data.text)

    # POST /t/add
    #content_str = "[from PySDK] %s says: %s" % (tweet1.data.nick, tweet1.data.origtext)
    #tweet2 = api.post.t__add(format="json", content=content_str, clientip="10.0.0.1")
    #print ">> time=%s, http://t.qq.com/p/t/%s" % (tweet2.data.time, tweet2.data.id)

    # GET /statuses/user_timeline
    #user_timeline = api.get.statuses__user_timeline(format="json", name="qqfarm", reqnum=1, pageflag=0, lastid=0, pagetime=0, type=3, contenttype=0)
    #for idx, tweet in enumerate(user_timeline.data.info):
    #    checkdir('weibo/' + tweet.name)
    #    f1 = file('weibo/' + tweet.name + '/' + tweet.id + '.pkl','wb')
    #    pickle.dump(tweet, f1, True)
    #    #print "[%d] http://t.qq.com/p/t/%s, (type:%d) %s" % (idx+1, tweet.id, tweet.type, tweet.text)

    users_timeline = api.get.statuses__public_timeline(format="json")
    #print users_timeline.data.user
    for i in users_timeline.data.user:
        try:
            gettimelie(api, i)
        except:
            print 'error'
    #    userlist.write(i + '\n')
    #    print time.time(), "Success!:", i
    #userlist.close()
    # UPLOAD /t/upload_pic
    #pic1 = api.upload.t__upload_pic(format="json", pic_type=2, pic=open(IMG_EXAMPLE, "rb"))
    #print ">> IMG: %s" % (pic1.data.imgurl)

    # POST /t/add_pic_url
    #content_str2 = "[from PySDK] add pic demo: %s, time %s" % (IMG_EXAMPLE, time.time())
    #pic_urls = "%s" % (pic1.data.imgurl)
    #tweet_pic1 = api.post.t__add_pic_url(format="json", content=content_str2, pic_url=pic_urls, clientip="10.0.0.1")
    #print ">> time=%s, http://t.qq.com/p/t/%s" % (tweet_pic1.data.time, tweet_pic1.data.id)

if __name__ == '__main__':
    #scheduler = sched.scheduler(time.time, time.sleep)
    #print 'START:', time.time()
    #for i in range(1,86400):
    #    scheduler.enter(i, 1, tweibo_test, ())
    ## access_token_test()
    ## tweibo_test()
    #scheduler.run()
    api = tweibo_api()
    print api.get.statuses__public_timeline(format="json")
    # print api.get.user__other_info(format="json",name="sos777")
