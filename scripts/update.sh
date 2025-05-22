#!/usr/bin/env zsh

# Notes
# printf employed due to presence of escape characters

FILEPATH="/Users/arwhyte/Development/github/arwhyte/dotfiles-m1/scripts"

set -e  # Exit immediately if a command exits with a non-zero status

printf "\nINFO: UPDATE ASTRAL UV AND UV TOOL (ALL)\n"
$FILEPATH/uv.sh

printf "\nINFO: UPDATE/UPGRADE HOMEBREW PACKAGES/CASKS\n"
$FILEPATH/brew.sh