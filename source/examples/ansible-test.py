{
    "ANSIBLE_MODULE_ARGS": {
        "query": """
             set debug=on;
             create table test.mock ('id','first_name','last_name','email','gender','ip_address')
             file='~/repos/chris17453/ddb/source/test/MOCK_DATA.csv';
             SELECT * FROM test.mock;
             "

        """,
    }
}