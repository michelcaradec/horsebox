#!/bin.bash

alias ll='ls -lh'

# Install curl
apt --yes update
apt --yes install curl

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# To update uv: `uv self update`
source $HOME/.local/bin/env

# Instal JQ
apt install --yes jq

cd /home/project
