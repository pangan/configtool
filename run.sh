#!/bin/sh
gunicorn --bind 0.0.0.0:8080 configtool:app --chdir /opt/configtool