#! /usr/bin/env python
# -*- coding:utf-8 -*- #
__author__ = 'liuzheng'

from tweibo import *
import ConfigParser
import os

# 返回text是unicode，设置默认编码为utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def tweibo_api():
    config = ConfigParser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config.ini').replace('\\', '/'))
    # 换成你的 APPKEY
    APP_KEY = config.get('APPKEY', 'APP_KEY')
    APP_SECRET = config.get('APPKEY', 'APP_SECRET')
    CALLBACK_URL = config.get('APPKEY', 'CALLBACK_URL')
    # 请先按照 https://github.com/upbit/tweibo-pysdk/wiki/OAuth2Handler 的鉴权说明填写 ACCESS_TOKEN 和 OPENID
    ACCESS_TOKEN = config.get('APPKEY', 'ACCESS_TOKEN')
    OPENID = config.get('APPKEY', 'OPENID')
    OPENKEY = config.get('APPKEY', 'OPENKEY')
    oauth = OAuth2Handler()
    oauth.set_app_key_secret(APP_KEY, APP_SECRET, CALLBACK_URL)
    oauth.set_access_token(ACCESS_TOKEN)
    oauth.set_openid(OPENID, OPENKEY)
    api = API(oauth)
    return api


def checkdir(path):
    if os.path.exists(path) == 0:
        os.mkdir(path)


def gettimelie(api, name):
    user_timeline = api.get.statuses__user_timeline(format="json", name=name,
                                                    reqnum=100, pageflag=0, lastid=0, pagetime=0, type=3, contenttype=0)
    # for idx, tweet in enumerate(user_timeline.data.info):
    #     checkdir('weibo/' + tweet.name)
    #     f1 = file('weibo/' + tweet.name + '/' + tweet.id + '.pkl','wb')
    #     pickle.dump(tweet, f1, True)
    return user_timeline


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
    data = api.get.statuses__public_timeline(format="json", reqnum=1)
    if data['ret'] == 0:
        user = []
        print 'get success'
        users = data['data']['info']
        for u in users:
            print u['text']
            user.append({'text': u['text'], 'count': u['count'], 'wid': u['id'], 'name': u['name'], 'uid': u['openid'],
                         'nick': u['nick'], 'self': u['self'], 'timestamp': u['timestamp'], 'type': u['type'],
                         'location': u['location'], 'country_code': u['country_code'],
                         'province_code': u['province_code'], 'city_code': u['city_code'], 'geo': u['geo'],
                         'emotionurl': u['emotionurl'], 'emotiontype': u['emotiontype']
            })
        print users[0]['openid']
    print user
    # print api.get.user__other_info(format="json",name="sos777")
