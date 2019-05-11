#!/bin/bash

for filename in dataset/*; do
	python detect.py --images $filename --det dataset_det/
done
