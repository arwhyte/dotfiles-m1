#!/usr/bin/env zsh?

# Notes
# printf employed due to presence of escape characters

FILEPATH="/Users/arwhyte/Development/github/arwhyte/dotfiles-m1/brew/Brewfile"

printf "INFO: HOMEBREW INSTALLED PACKAGES/CASKS (brew list)\n"
brew list

printf "\nINFO: HOMEBREW OUTDATED PACKAGES/CASKS (brew outdated))\n"
brew outdated

printf "\nINFO: AUTOREMOVE UNUSED PACKAGE DEPENDENCIES (brew autoremove) \n"
brew autoremove

printf "\nINFO: UPDATE HOMEBREW PACKAGES/CASKS (brew update)\n"
brew update

printf "\nINFO: UPGRADE HOMEBREW PACKAGES/CASKS (brew upgrade)\n"
brew upgrade

printf "\nINFO: CHECK HOMEBREW INSTALLS (brew doctor)\n"
brew doctor

printf "\nINFO: CLEANUP HOMEBREW (brew cleanup)\n"
brew cleanup

printf "\nINFO: DUMP HOMEBREW INSTALLS TO $FILEPATH (brew bundle dump)\n"
brew bundle dump --force --file=$FILEPATH

printf "\nINFO: HOMEBREW MANAGED SERVICES (brew services list)\n"
brew services list
