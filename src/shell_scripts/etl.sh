#! /bin/bash

mkdir -p notebook/data
(docker run -itv $PWD:/code \
            -w /code python:3.7 \
            /bin/bash -c "(bash shell_scripts/create_env.sh && source .venv/bin/activate && cd etl && python etl.py)")

mv etl/data/casetable.psv notebook/data/casetable.psv