import os


paths=[ "~/repos/chris17453/ddb/source/test/MOCK_DATA.csv",
        "/home/cwatkin1/repos/chris17453/ddb/test/data/MOCK_DATA.csv",
        "source/test/MOCK_DATA.csv",
        "../ddb/source/test/MOCK_DATA.csv",
        "bob"]


for path in paths:
    print (os.path.abspath(os.path.expanduser(path)))
