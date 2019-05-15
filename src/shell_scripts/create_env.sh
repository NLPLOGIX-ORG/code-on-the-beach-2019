#!/bin/bash
(python3 -m venv .venv && source .venv/bin/activate && cd etl && python -m pip install --upgrade pip && python -m pip install -r requirements.txt)