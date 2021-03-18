



```
# 创建数据库ecspider
create database ecspider character set utf8;
# 创建用户名为ecspider，密码为ecspider
create user 'ecspider'@'%' identified by 'ecspider';
# 赋予用户ecspider操作数据库ecspider的所有权限
grant all privileges on ecspider.* to 'ecspider'@'%';
flush privileges;
```



```mysql
create table users(
userid int(11) not null auto_increment,
username varchar(20) not null,
password varchar(16) not null,
email varchar(20) default null,
phonenumber varchar(11) default null,
nickname varchar(20) default null,
sex char(1) default null,
primary key(userid)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;



create table goods(
goodid varchar(20) not null,
platform varchar(5) not null,
title varchar(100) not null,
price float not null,
msales int(8) not null default 0,
shopname varchar(20),
href varchar(50) not null,
picpath varchar(30),
tags varchar(100),
primary key(goodid)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table watchlist(
userid int(11) not null,
goodid varchar(20) not null,
platform varchar(5) not null,
nowprice float not null,
lowprice float not null,
highprice float not null,
href varchar(50) not null,
picpath varchar(30),
FOREIGN KEY (userid) REFERENCES users(userid),
FOREIGN KEY (goodid) REFERENCES goods(goodid),
primary key(userid, goodid)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table records(
userid int(11) not null,
searchterm varchar(20) not null,
wordcloud varchar(100),
wcpath varchar(20),
tags varchar(100),
primary key(userid)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
```





```mysql
insert into users (userid, username, password, nickname, sex)
values (default, 'cwolf9', '123456','李行', '男');
```



