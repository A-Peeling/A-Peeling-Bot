#!/usr/bin/env bash
echo "creating virtualenv"
python3 -m venv ./venv
source ./venv/bin/activate
echo "installing dependencies..."
python3 -m pip -U install discord.py requests
echo "done! you can now run the bot."
