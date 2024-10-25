#!/bin/bash

# Command options
# -s create symbolic link
# -f continue with other symlinking if error occurs
# -n avoid symlinking a symlink

# git
rm -rf /Users/arwhyte/.gitconfig
ln -nfs /Users/arwhyte/Development/github/arwhyte/dotfiles-m1/git/.gitconfig /Users/arwhyte/.gitconfig
# rm -rf /Users/arwhyte/.gitconfig.local
# ln -nfs /Users/arwhyte/Development/github/arwhyte/dotfiles-m1/git/.gitconfig.local /Users/arwhyte/.gitconfig.local
# rm -rf /Users/arwhyte/.gitignore.global
# ln -nfs /Users/arwhyte/Development/github/arwhyte/dotfiles-m1/git/.gitignore.global /Users/arwhyte/.gitignore.global

# psql
rm -rf /Users/arwhyte/.psqlrc
ln -nfs /Users/arwhyte/Development/github/arwhyte/dotfiles-m1/psql/.psqlrc /Users/arwhyte/.psqlrc

# zsh
rm -rf /Users/arwhyte/.zprofile
ln -nfs /Users/arwhyte/Development/github/arwhyte/dotfiles-m1/zsh/.zprofile /Users/arwhyte/.zprofile
rm -rf /Users/arwhyte/.zshenv
ln -nfs /Users/arwhyte/Development/github/arwhyte/dotfiles-m1/zsh/.zshenv /Users/arwhyte/.zshenv
rm -rf /Users/arwhyte/.zshrc
ln -nfs /Users/arwhyte/Development/github/arwhyte/dotfiles-m1/zsh/.zshrc /Users/arwhyte/.zshrc
