# nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # loads nvm bash_completion

# RETIRED pyenv
# export PYENV_ROOT="$HOME/.pyenv"
# [[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"

# RETIRED pipx
# https://pipx.pypa.io/stable/installation/

# export PATH="$PATH:/Users/arwhyte/.local/bin"
# export PIPX_HOME="$HOME/.local/pipx"

# Rust
[[ -f "$HOME/.cargo/env" ]] && . "$HOME/.cargo/env"
# . "$HOME/.cargo/env"