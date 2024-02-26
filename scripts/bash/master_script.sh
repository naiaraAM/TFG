#!/bin/bash

./process_malware.sh
cd ..
cd python/
python3 compare.py
cd ../../db
python3 creation.py
python3 insertion.py
python3 comparison.py
