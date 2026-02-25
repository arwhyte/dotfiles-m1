#!/usr/bin/env zsh?


# Command options
# -s create symbolic link
# -f continue with other symlinking if error occurs
# -n avoid symlinking a symlink

# Base Paths
HOME="/Users/arwhyte"
BASE_PATH="${HOME}/Development/github/arwhyte/dotfiles-m1"

# brew
rm -rf ${HOME}/brew.sh
ln -nfs ${BASE_PATH}/scripts/brew.sh ${HOME}/brew.sh

# git
rm -rf ${HOME}/.gitconfig
ln -nfs ${BASE_PATH}/git/.gitconfig ${HOME}/.gitconfig
# rm -rf ${HOME}/.gitconfig.local
# ln -nfs ${BASE_PATH}/git/.gitconfig.local ${HOME}/.gitconfig.local
# rm -rf ${HOME}/.gitignore.global
# ln -nfs ${BASE_PATH}/git/.gitignore.global ${HOME}/.gitignore.global

# psql
rm -rf ${HOME}/.psqlrc
ln -nfs ${BASE_PATH}/psql/.psqlrc ${HOME}/.psqlrc

# scripts
rm -rf ${HOME}/update.sh
ln -nfs ${BASE_PATH}/scripts/update.sh ${HOME}/update.sh
rm -rf ${HOME}/pg_upgrade.py
ln -nfs ${BASE_PATH}/scripts/pg_upgrade.py ${HOME}/pg_upgrade.py
rm -rf ${HOME}/update.py
ln -nfs ${BASE_PATH}/scripts/update.py ${HOME}/update.py

# zsh
rm -rf ${HOME}/.zprofile
ln -nfs ${BASE_PATH}/zsh/.zprofile ${HOME}/.zprofile
rm -rf ${HOME}/.zshenv
ln -nfs ${BASE_PATH}/zsh/.zshenv ${HOME}/.zshenv
rm -rf ${HOME}/.zshrc
ln -nfs ${BASE_PATH}/zsh/.zshrc ${HOME}/.zshrc
