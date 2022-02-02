#!/bin/bash

eval "$(conda shell.bash hook)"
conda activate temp_mon
uwsgi --http-socket :5000 --module wsgi:app

