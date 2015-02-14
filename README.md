# Installation

```sh
$ sudo apt-get install python-setuptools
$ sudo easy_install pip
$ sudo pip install mysql-replication
$ sudo pip install redis
```

#Example
```sh
mysql> create database contact;

mysql> use contact;

mysql> create table contactinfo (fname varchar(20), lname varchar(20));

mysql> insert into contactinfo values ('Rakesh','Rathi');

mysql> update contactinfo set fname='Jai' where fname='Rakesh';
```

```sh
$ sudo python mysql-redis-sync.py
[Insert] SQLBinLog Row :{'values': {u'lname': u'Rathi', u'fname': u'Rakesh'}}
Updated Cache -> contact-contactinfo-lname : Rathi
Updated Cache -> contact-contactinfo-fname : Rakesh
[Update] SQLBinLog Row :{'before_values': {u'lname': u'Rathi', u'fname': u'Rakesh'}, 'after_values': {u'lname': u'Rathi', u'fname': u'Jai'}}
Updated Cache -> contact-contactinfo-fname : Jai
```
