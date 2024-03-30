eval "$(/opt/homebrew/bin/brew shellenv)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Brewfile
export HOMEBREW_BREWFILE="$HOME/Development/github/arwhyte/dotfiles-m1/brew/Brewfile"

# GPG setup
export GPG_TTY=$(tty)
# GPG_TTY=$TTY

# nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # loads nvm bash_completion

# pyenv
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"

# pipx
# https://pipx.pypa.io/stable/installation/
export PATH="$PATH:/Users/arwhyte/.local/bin"
export PIPX_HOME="$HOME/.local/pipx"

# Homebrew Python (Apple silicon)
# export PATH="/opt/homebrew/opt/python@3.12/libexec/bin:$PATH"
# export PATH="/opt/homebrew/opt/python@3.11/libexec/bin:$PATH"
# export PATH="/opt/homebrew/opt/python@3.10/libexec/bin:$PATH"

# Aliases
if [ -f ~/Development/github/arwhyte/dotfiles-m1/zsh/.aliases ]; then
    source ~/Development/github/arwhyte/dotfiles-m1/zsh/.aliases
else
    print "ERROR: ~/Development/github/arwhyte/dotfiles-m1/zsh/.aliases not found."
fi
