#!/usr/bin/env bash
# fuck the crontab
env | sed 's/^\([^=]*\)=\(.*\)$/\1="\2"/g' > envs.py
supervisord --nodaemon
