#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2014
# Gmail:liuzheng712
#


def fileRead(sql, user):
    import cPickle as pickle
    import os,sys
    import logging
    import time
    logging.basicConfig(filename='tweibo.log',level=logging.DEBUG)
    weibo = os.listdir('ww/'+user)
    curs = sql.cursor()
    try:
        userInfo(sql, user)
    except:
        logging.warning('Can\'t Insert UserInfo %s ,User maybe does not exist',user)
    sql.select_db('tweibo')
    for filename in weibo:
        f1 = file('ww/' + user + '/' + filename,'rb')
        tw = pickle.load(f1)
        curs.execute("select weiboid from weibo where weiboid=%s;",[tw.id])
        result = curs.fetchall()
        if len(result) > 0:
            continue
        tweibo = [tw.id, tw.name, tw.nick, tw.city_code, tw.count,
            tw.country_code, tw.emotiontype, tw.emotionurl, matchFrom(tw), tw.fromurl,
            tw.geo, tw.head, tw.https_head, str(tw.image), tw.isrealname, tw.isvip,
            tw.jing, tw.latitude, tw.location, tw.longitude, tw.mcount, tw.music,
            tw.openid, tw.origtext, tw.province_code, tw.readcount, tw.self,
            tw.source, tw.status, tw.text, tw.timestamp, tw.type, tw.video, tw.wei]
        #print tweibo
        if len(str(tw.image)) > 5:
            try:
                picInsert(sql, tw.pic)
            except:
                logging.warning('Can\'t Insert User %s pic:weiboID %s from file %s',tw.name,tw.id,filename)
        try:
            curs.execute("insert into weibo values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",tweibo)
            #sql.commit()
        except:
            logging.warning('Can\'t Insert User %s:weiboID %s from file %s',tw.name,tw.id,filename)

    #print tweet.name, '==', tweet.nick, '=='


def userInfo(sql, name):
    curs = sql.cursor()
    sql.select_db('tweibo')
    curs.execute("select name from userInfo where name=%s;", [name])
    result = curs.fetchall()
 #   print len(result)
    if len(result) > 0: 
        return 1
    import demo
    api = demo.tweibo_api()
    user_info = api.get.user__other_info(format="json",name=name)
    ui = user_info.data
    userinfo = [ui.name, ui.nick, ui.location, ui.sex, ui.email, ui.birth_day,
            ui.birth_month, ui.birth_year, ui.city_code, ui.comp,
            ui.country_code, ui.edu, ui.exp, ui.fansnum, ui.favnum, ui.head,
            ui.homecity_code, ui.homecountry_code, ui.homepage,
            ui.homeprovince_code, ui.hometown_code, ui.https_head, ui.idolnum,
            ui.industry_code, ui.introduction, ui.isent, ui.ismyblack,
            ui.ismyfans, ui.ismyidol, ui.isrealname, ui.isvip, ui.level,
            ui.mutual_fans_num, ui.openid, ui.province_code, ui.regtime,
            ui.send_private_flag, ui.tweetnum, ui.verifyinfo ]
    try:
        curs.execute("insert into userInfo values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",userinfo)
        #sql.commit()
        return 1
    except:
        return 0


def picInsert(sql, pic):
    curs = sql.cursor()
    sql.select_db('tweibo')
    for p in pic.info:
        curs.execute("select url from pic where url=%s;",[p.url])
        result = curs.fetchall()
        if len(result) > 0:
            continue
        pInfo = [p.url, p.pic_YDPI, p.pic_type, p.pic_height, p.pic_XDPI,
                p.pic_width, p.pic_size]
        curs.execute("insert into pic values(%s,%s,%s,%s,%s,%s,%s);",pInfo)
        #sql.commit()
    return 1



def matchFrom(tw):
    import re
    pattern = re.compile(r"from\'.*?\'(.*?)\'")
    #print pattern.search(str(tw)).group(1).decode('unicode-escape')
    return pattern.search(str(tw)).group(1).decode('unicode-escape')

def mysql():
    import MySQLdb
    import cPickle as pickle
    import ConfigParser
    #f1 = file('ww/sos777/238240103807467.pkl','rb')
    #tweet = pickle.load(f1)
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    host = config.get('MySQL', 'host')
    user = config.get('MySQL', 'username')
    port = config.get('MySQL', 'port') 
    passwd = config.get('MySQL', 'passwd')
    sql = MySQLdb.connect(host=host, user=user, passwd=passwd, port=int(port), charset='utf8')
    #curs = sql.cursor()
    #curs.execute("create database pythondb")
    #conn.select_db('pythondb')
    #sql.select_db('tweibo')
    #curs.execute("create table test(id int,message varchar(50))")
    #value = [1,"davehe"]
    #curs.execute("insert into userInfo values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",userInfo("sos777"))
    #sql.commit()
    #curs.close()
    #userInfo(sql, 'sos777')
#    print "done!"
    return sql


if __name__ == "__main__":
    #mysql()
    import os,sys
    #import cPickle as pickle
    #import re
    import logging
    import time
    logging.basicConfig(filename='tweibo.log',level=logging.DEBUG)
    logging.warning("################Start at %s ################",time.localtime(time.time()))
    sql = mysql()
    weibo = os.listdir('ww')
    for ren in weibo[weibo.index('chenzhiyun9683'):]:
        #print ren
        fileRead(sql, ren)
        #mysql(ren)
    sql.commit()
    sql.close()
    print "done"
    #ren = os.listdir('ww/' + weibo[0]  )
    ##print (file('ww/' + weibo[0] +'/'+ren[1],'rb'))
    #tw = pickle.load(file('ww/' + weibo[0] +'/'+ren[1],'rb'))
    #print userInfo('sos777')

