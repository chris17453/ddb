#!/bin/bash

# TODO make this ... better

gprof2dot -f pstats $1 | dot -Tpng -o $2