#!/bin/bash

rm para/*.npy

python3 src/inner_para.py
python3 src/getRGBD.py
