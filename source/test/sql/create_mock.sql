drop table mock.test;
create table mock.test 
('id','first_name','last_name','email','gender','ip_address') 
file='source/test/MOCK_DATA.csv'
delimiter=','
data_starts_on='2'
