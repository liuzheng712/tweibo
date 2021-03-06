drop database if exists tweibo;
create database tweibo character set utf8;
use tweibo;
create table userInfo
(
  name char(20) not null primary key,
  nick text not null,
  location text,
  sex int(2) ,
  email char(40),
  birth_day char(20),
  birth_month char(20),
  birth_year char(20),
  city_code char(20),
  comp text,
  country_code char(20),
  edu text,
  exp char(20),
  fansnum char(20),
  favnum char(20),
  head char(90),
  homecity_code char(20),
  homecountry_code char(20),
  homepage text,
  homeprovince_code char(20),
  hometown_code char(20),
  https_head char(80),
  idolnum char(20),
  industry_code char(20),
  introduction text,
  isent char(4),
  ismyblack char(4),
  ismyfans char(4),
  ismyidol char(4),
  isrealname char(4),
  isvip char(4),
  level char(4),
  mutual_fans_num char(20),
  openid char(32),
  province_code char(20),
  regtime char(20),
  send_private_flag char(4),
  tweetnum char(20),
  verifyinfo text
)DEFAULT CHARSET=utf8;

create table weibo
(
  weiboid char(25) primary key,
  name char(30),
  nick text,
  city_code char(10),
  count char(10),
  country_code char(10),
  emotiontype char(10),
  emotionurl text,
  t_from char(25),
  fromurl text,
  geo text,
  head char(70),
  https_head char(80),
  image text,
  isrealname char(4),
  isvip char(4),
  jing char(10),
  latitude char(75),
  location text,
  longitude char(75),
  mcount char(4),
  music text,
  openid char(50),
  origtext text,
  province_code char(4),
  readcount char(10),
  self char(4),
  source text,
  status char(4),
  t_text text,
  t_timestamp char(14),
  type char(4),
  video text,
  wei char(10)
)DEFAULT CHARSET=utf8;

create table pic
(
  url char(70) primary key,
  pic_XDPI char(10),
  pic_YDPI char(10),
  pic_height char(10),
  pic_size char(10),
  pic_type char(10),
  pic_width char(10)  
)DEFAULT CHARSET=utf8;
