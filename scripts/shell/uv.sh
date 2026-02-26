#!/usr/bin/env zsh

# Notes
# printf employed due to presence of escape characters

printf "\nINFO: UPDATE UV\n"
uv self update

printf "\nINFO: UPDATE UV TOOLS\n"
uv tool update --all

printf "\n"