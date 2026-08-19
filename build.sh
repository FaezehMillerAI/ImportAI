#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install --upgrade pip
pip install --retries 10 --timeout 60 -r requirements.txt
