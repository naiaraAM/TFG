#!/bin/bash

./process_basic_info.sh
cd ..
cd python/
python3 compare.py
cd ../../db
python3 creation.py
python3 insertion.py
python3 comparison.py
