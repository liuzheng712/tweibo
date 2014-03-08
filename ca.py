#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2013
# Gmail:liuzheng712
#


#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cassandra.cluster import Cluster
import logging
import time

log = logging.getLogger()
log.setLevel('INFO')

class SimpleClient:
    session = None

    def connect(self, nodes):
        cluster = Cluster(nodes)
        metadata = cluster.metadata
        self.session = cluster.connect()
        log.info('Connected to cluster: ' + metadata.cluster_name)
        for host in metadata.all_hosts():
            log.info('Datacenter: %s; Host: %s; Rack: %s',
                host.datacenter, host.address, host.rack)

    def close(self):
        self.session.cluster.shutdown()
        self.session.shutdown()
        log.info('Connection closed.')


    def create_schema(self):
        self.session.execute("""CREATE KEYSPACE tweibo WITH replication = {'class':'SimpleStrategy', 'replication_factor':3};""")
        self.session.execute("""
            CREATE TABLE tweibo.userInfo(
                id uuid PRIMARY KEY,
                name text,
                nick text,
                location text,
                ex text, 
                email text,
                birth_day text,
                birth_month text,
                birth_year text,
                city_code text,
                comp text,
                country_code text,
                edu text,
                exp text,
                fansnum text,
                favnum text,
                head text,
                homecity_code text,
                homecountry_code text,
                homepage text,
                homeprovince_code text,
                hometown_code text,
                https_head text,
                idolnum text,
                industry_code text,
                introduction text,
                isent text,
                ismyblack text,
                ismyfans text,
                ismyidol text,
                isrealname text,
                isvip text,
                level text,
                mutual_fans_num text,
                openid text,
                province_code text,
                regtime text,
                send_private_flag text,
                tweetnum text,
                verifyinfo text
            );
        """)
        self.session.execute("""
            CREATE TABLE tweibo.weibo(
                id uuid,
                weiboid text,
                name text,
                nick text,
                city_code text,
                count text,
                country_code text,
                emotiontype text,
                emotionurl text,
                t_from text,
                fromurl text,
                geo text,
                head text,
                https_head text,
                image text,
                isrealname text,
                isvip text,
                jing text,
                latitude text,
                location text,
                longitude text,
                mcount text,
                music text,
                openid text,
                origtext text,
                province_code text,
                readcount text,
                self text,
                source text,
                status text,
                t_text text,
                t_timestamp text,
                type text,
                video text,
                wei text,
                PRIMARY KEY (id, weiboid, name)
            );
        """)
        self.session.execute("""
            CREATE TABLE tweibo.pic(
                url primary text,
                pic_XDPI text,
                pic_YDPI text,
                pic_height text,
                pic_size text,
                pic_type text,
                pic_width text,
                PRIMARY KEY (url)
            )
                """)
        log.info('tweibo keyspace and schema created.')


    def load_data(self):
        self.session.execute("""
            INSERT INTO tweibo.songs (id, title, album, artist, tags)
            VALUES (
                756716f7-2e54-4715-9f00-91dcbea6cf50,
                'La Petite Tonkinoise',
                'Bye Bye Blackbird',
                'Joséphine Baker',
                {'jazz', '2013'}
            );
        """)
        self.session.execute("""
            INSERT INTO tweibo.playlists (id, song_id, title, album, artist)
            VALUES (
                2cc9ccb7-6221-4ccb-8387-f22b6a1b354d,
                756716f7-2e54-4715-9f00-91dcbea6cf50,
                'La Petite Tonkinoise',
                'Bye Bye Blackbird',
                'Joséphine Baker'
            );
        """)
        log.info('Data loaded.')

    def query_schema(self):
        results = self.session.execute("""
    SELECT * FROM tweibo.playlists
    WHERE id = 2cc9ccb7-6221-4ccb-8387-f22b6a1b354d;
""")
        print "%-30s\t%-20s\t%-20s\n%s" % \
                ("title", "album", "artist",
                        "-------------------------------+-----------------------+--------------------")
                for row in results:
                    print "%-30s\t%-20s\t%-20s" % (row.title, row.album, row.artist)
        log.info('Schema queried.')

def main():
    logging.basicConfig()
    client = SimpleClient()
    client.connect(['192.168.1.47'])
    client.create_schema()
    time.sleep(10)
    #client.load_data()
    #client.query_schema()
    client.close()

if __name__ == "__main__":
    main()
