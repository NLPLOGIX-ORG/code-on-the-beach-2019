#! /bin/bash

(docker run -itv $PWD:/code \
            -w /code python:3.7 \
            /bin/bash -c "(bash shell_scripts/create_env.sh && source .venv/bin/activate && cd etl && python etl.py)")