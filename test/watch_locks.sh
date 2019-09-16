#!/bin/bash

watch -n .1 'cat  test/data/MOCK_DATA_LOCKING.csv   | cut -d ',' -f 2 | sort|uniq -c'
