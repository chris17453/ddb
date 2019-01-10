### ddb Walkthrough


```sql
[test]$ddb

Welcome! Type ? to list commands
ddb> use test_db
┌┤changed_db                                                                             ├┐
│test_db                                                                                  │
└[changed_db                                                                             ]┘
>>> executed in 0.00117802619934 seconds 

ddb> create table mock (id,first_name,last_name,email,gender,ip_address) file='ddb/test/MOCK_DATA.csv' delimiters=','
┌┤create table                                                                           ├┐
│1                                                                                        │
└[create table                                                                           ]┘
>>> executed in 0.225665092468 seconds 

ddb> show tables
┌┤database                                   ├┬┤table                                    ├┐
│main                                         │test                                       │
│test_db                                      │mock                                       │
└[database                                   ]┴[table                                    ]┘
>>> executed in 0.00108098983765 seconds 

ddb> show columns from mock
┌┤table                                      ├┬┤column                                   ├┐
│mock                                         │id                                         │
│mock                                         │first_name                                 │
│mock                                         │last_name                                  │
│mock                                         │email                                      │
│mock                                         │gender                                     │
│mock                                         │ip_address                                 │
└[table                                      ]┴[column                                   ]┘
>>> executed in 0.00223302841187 seconds 

ddb> select * from mock limit 10
select * from mock limit 10
┌┤id          ├┬┤first_name  ├┬┤last_name   ├┬┤email       ├┬┤gender      ├┬┤ip_address  ├┐
│id            │first_name    │last_name     │email         │gender        │ip_address    │
│1             │Say           │Murgatroyd    │smurgatroyd0@u│Male          │35.226.127.123│
│2             │Redford       │Ornils        │rornils1@amazo│Male          │24.42.186.82  │
│3             │Grenville     │Buckley       │gbuckley2@gizm│Male          │143.223.126.20│
│4             │Thalia        │Badrock       │tbadrock3@xinh│Female        │113.57.179.78 │
│5             │Julie         │Minchell      │jminchell4@sky│Female        │105.165.149.12│
│6             │Lancelot      │Archibold     │larchibold5@pi│Male          │213.155.189.44│
│7             │Bernie        │Matteucci     │bmatteucci6@br│Male          │109.156.49.36 │
│8             │Flinn         │Mulchrone     │fmulchrone7@na│Male          │22.84.116.46  │
│9             │Seamus        │Tocque        │stocque8@cnet.│Male          │79.30.35.75   │
└[id          ]┴[first_name  ]┴[last_name   ]┴[email       ]┴[gender      ]┴[ip_address  ]┘
>>> executed in 0.00982999801636 seconds 

ddb> update mock set id=1001 where id=1
┌┤updated                                                                                ├┐
│1                                                                                        │
└[updated                                                                                ]┘
>>> executed in 0.00821018218994 seconds 

ddb> select * from mock where id=1001
┌┤id          ├┬┤first_name  ├┬┤last_name   ├┬┤email       ├┬┤gender      ├┬┤ip_address  ├┐
│1001          │Say           │Murgatroyd    │smurgatroyd0@u│Male          │35.226.127.123│
└[id          ]┴[first_name  ]┴[last_name   ]┴[email       ]┴[gender      ]┴[ip_address  ]┘
>>> executed in 0.0078330039978 seconds 

ddb> delete from mock where id=1001
┌┤deleted                                                                                ├┐
│1                                                                                        │
└[deleted                                                                                ]┘
>>> executed in 0.00804209709167 seconds 

ddb> select * from mock where id=1001
┌┤id          ├┬┤first_name  ├┬┤last_name   ├┬┤email       ├┬┤gender      ├┬┤ip_address  ├┐
└[id          ]┴[first_name  ]┴[last_name   ]┴[email       ]┴[gender      ]┴[ip_address  ]┘
>>> executed in 0.00705003738403 seconds 

ddb> insert into  mock (id,first_name,last_name,email,gender,ip_address) values(1,n1,n2,'sam#sam.com',Male,'0.0.0.0')
┌┤inserted                                                                               ├┐
│1                                                                                        │
└[inserted                                                                               ]┘
>>> executed in 0.015517950058 seconds 

ddb> select * from mock where id=1
┌┤id          ├┬┤first_name  ├┬┤last_name   ├┬┤email       ├┬┤gender      ├┬┤ip_address  ├┐
│1             │n1            │n2            │sam#sam.com   │Male          │0.0.0.0       │
└[id          ]┴[first_name  ]┴[last_name   ]┴[email       ]┴[gender      ]┴[ip_address  ]┘
>>> executed in 0.00686001777649 seconds 

ddb> select * from mock limit 10
┌┤id          ├┬┤first_name  ├┬┤last_name   ├┬┤email       ├┬┤gender      ├┬┤ip_address  ├┐
│id            │first_name    │last_name     │email         │gender        │ip_address    │
│2             │Redford       │Ornils        │rornils1@amazo│Male          │24.42.186.82  │
│3             │Grenville     │Buckley       │gbuckley2@gizm│Male          │143.223.126.20│
│4             │Thalia        │Badrock       │tbadrock3@xinh│Female        │113.57.179.78 │
│5             │Julie         │Minchell      │jminchell4@sky│Female        │105.165.149.12│
│6             │Lancelot      │Archibold     │larchibold5@pi│Male          │213.155.189.44│
│7             │Bernie        │Matteucci     │bmatteucci6@br│Male          │109.156.49.36 │
│8             │Flinn         │Mulchrone     │fmulchrone7@na│Male          │22.84.116.46  │
│9             │Seamus        │Tocque        │stocque8@cnet.│Male          │79.30.35.75   │
│10            │Lazare        │Abbett        │labbett9@who.i│Male          │17.173.76.145 │
└[id          ]┴[first_name  ]┴[last_name   ]┴[email       ]┴[gender      ]┴[ip_address  ]┘
>>> executed in 0.00780391693115 seconds 

ddb> select * from mock order by id limit 10
┌┤id          ├┬┤first_name  ├┬┤last_name   ├┬┤email       ├┬┤gender      ├┬┤ip_address  ├┐
│1             │n1            │n2            │sam#sam.com   │Male          │0.0.0.0       │
│10            │Lazare        │Abbett        │labbett9@who.i│Male          │17.173.76.145 │
│100           │Eleanor       │Heditch       │eheditch2r@ocn│Female        │124.231.187.47│
│1000          │Curcio        │Kemm          │ckemmrr@irs.go│Male          │14.143.73.253 │
│10003         │test_name1    │test_lname    │sam@bob.com   │male          │0.0.0.0       │
│101           │Curry         │Kerkham       │ckerkham2s@app│Male          │139.216.9.172 │
│102           │Joanna        │Simone        │jsimone2t@dion│Female        │48.225.191.89 │
│103           │Giffie        │Aikin         │gaikin2u@noaa.│Male          │9.169.172.177 │
│104           │Rosalinda     │Hedin         │rhedin2v@aol.c│Female        │239.132.244.29│
│105           │Jolyn         │Smy           │jsmy2w@deviant│Female        │220.24.157.8  │
└[id          ]┴[first_name  ]┴[last_name   ]┴[email       ]┴[gender      ]┴[ip_address  ]┘
>>> executed in 0.00986289978027 seconds 

```
