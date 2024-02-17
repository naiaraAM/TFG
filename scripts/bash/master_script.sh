#!/bin/bash

./process_malware.sh
cd ../../db
python3 creation.py
python3 insertion.py