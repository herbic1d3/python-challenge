#!/bin/bash

echo Creating environment
pyvenv-3.4 venv


echo Installing dependencies
pyvenv-3.4 venv && ./venv/bin/pip install -r ./pipreq.txt

