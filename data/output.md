## ddb CLI Output examples
You can specify the output type 
- bash 
- term
- xml
- yaml
- json

```bash
(ddb) [nd@nd-dm ddb]$ dist/ddb 'use test;select * from mock where id='1' or id='3' order by id desc limit 10' -o raw
```
```bash
3,Grenville,Buckley,gbuckley2@gizmodo.com,Male,143.223.126.204
1,n1,n2,sam#sam.com,Male,0.0.0.0
```


```bash
(ddb) [nd@nd-dm ddb]$ dist/ddb 'use test;select * from mock where id='1' or id='3' order by id desc limit 10' -o xml
```
```xml
<?xml version="1.0" encoding="utf-8"?><data><results><raw><![CDATA[3,Grenville,Buckley,gbuckley2@gizmodo.com,Male,143.223.126.204]]></raw><type><![CDATA[3]]></type><data><![CDATA[3]]></data><data><![CDATA[Grenville]]></data><data><![CDATA[Buckley]]></data><data><![CDATA[gbuckley2@gizmodo.com]]></data><data><![CDATA[Male]]></data><data><![CDATA[143.223.126.204]]></data><error><![CDATA[]]></error></results><results><raw><![CDATA[1,n1,n2,sam#sam.com,Male,0.0.0.0]]></raw><type><![CDATA[3]]></type><data><![CDATA[1]]></data><data><![CDATA[n1]]></data><data><![CDATA[n2]]></data><data><![CDATA[sam#sam.com]]></data><data><![CDATA[Male]]></data><data><![CDATA[0.0.0.0]]></data><error><![CDATA[]]></error></results><columns><![CDATA[id]]></columns><columns><![CDATA[first_name]]></columns><columns><![CDATA[last_name]]></columns><columns><![CDATA[email]]></columns><columns><![CDATA[gender]]></columns><columns><![CDATA[ip_address]]></columns></data>
```

```bash
(ddb) [nd@nd-dm ddb]$ dist/ddb 'use test;select * from mock where id='1' or id='3' order by id desc limit 10' -o json
```
```json
{"results": [{"raw": "3,Grenville,Buckley,gbuckley2@gizmodo.com,Male,143.223.126.204", "type": 3, "data": ["3", "Grenville", "Buckley", "gbuckley2@gizmodo.com", "Male", "143.223.126.204"], "error": null}, {"raw": "1,n1,n2,sam#sam.com,Male,0.0.0.0", "type": 3, "data": ["1", "n1", "n2", "sam#sam.com", "Male", "0.0.0.0"], "error": null}], "columns": ["id", "first_name", "last_name", "email", "gender", "ip_address"]}
```

```bash
(ddb) [nd@nd-dm ddb]$ dist/ddb 'use test;select * from mock where id='1' or id='3' order by id desc limit 10' -o yaml
```
```yaml
columns:
- id
- first_name
- last_name
- email
- gender
- ip_address
results:
- data:
  - '3'
  - Grenville
  - Buckley
  - gbuckley2@gizmodo.com
  - Male
  - 143.223.126.204
  error: null
  raw: 3,Grenville,Buckley,gbuckley2@gizmodo.com,Male,143.223.126.204
  type: 3
- data:
  - '1'
  - n1
  - n2
  - sam#sam.com
  - Male
  - 0.0.0.0
  error: null
  raw: 1,n1,n2,sam#sam.com,Male,0.0.0.0
  type: 3
  ```

```bash
(ddb) [nd@nd-dm ddb]$ dist/ddb 'use test;select * from mock where id='1' or id='3' order by id desc limit 10' -o term
```
```bash
┌┤id                  ├┬┤first_name          ├┬┤last_name           ├┬┤email               ├┬┤gender              ├┬┤ip_address          ├┐
│3                     │Grenville             │Buckley               │gbuckley2@gizmodo.com │Male                  │143.223.126.204       │
│1                     │n1                    │n2                    │sam#sam.com           │Male                  │0.0.0.0               │
└[id                  ]┴[first_name          ]┴[last_name           ]┴[email               ]┴[gender              ]┴[ip_address          ]┘
```

```bash
(ddb) [nd@nd-dm ddb]$ dist/ddb 'use test;select * from mock where id='1' or id='3' order by id desc limit 10' -o bash
```
```bash
# bash variable assignment for ddb output
declare ddb_data -A
declare ddb_info -A
declare ddb_columns -A

ddb_columns[0]='id'
ddb_columns[1]='first_name'
ddb_columns[2]='last_name'
ddb_columns[3]='email'
ddb_columns[4]='gender'
ddb_columns[5]='ip_address'
ddb_info[0,error]=''
ddb_info[0,type]='3'
ddb_info[0,raw]='3,Grenville,Buckley,gbuckley2@gizmodo.com,Male,143.223.126.204'
ddb_data[0,0]='3'
ddb_data[0,1]='Grenville'
ddb_data[0,2]='Buckley'
ddb_data[0,3]='gbuckley2@gizmodo.com'
ddb_data[0,4]='Male'
ddb_data[0,5]='143.223.126.204'
ddb_info[1,error]=''
ddb_info[1,type]='3'
ddb_info[1,raw]='1,n1,n2,sam#sam.com,Male,0.0.0.0'
ddb_data[1,0]='1'
ddb_data[1,1]='n1'
ddb_data[1,2]='n2'
ddb_data[1,3]='sam#sam.com'
ddb_data[1,4]='Male'
ddb_data[1,5]='0.0.0.0'
# end ddb output 
```
