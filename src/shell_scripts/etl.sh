#! /bin/bash

(cd etl && docker run -itv $PWD:/code \
                      -w /code python:3.7 \
                      /bin/bash -c "(python3 -m pip install -r requirements.txt && python etl.py)")