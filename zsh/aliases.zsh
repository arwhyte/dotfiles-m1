# Interactive aliases & helpers only

[[ -o interactive ]] || return

# Directory paths (do NOT set HOME)
DEV="$HOME/Development"
DOCS="$HOME/Documents"
DROPBOX="$HOME/Library/CloudStorage/Dropbox-Personal"
PICS="$HOME/Pictures"

GITHUB="$DEV/github"
ARWHYTE="$GITHUB/arwhyte"
CSEV="$GITHUB/csev"
UMSI="$GITHUB/umsi-arwhyte"

# Brew
alias brew_bundle_install='brew bundle install --file="$GITHUB/arwhyte/dotfiles-m1/brew/Brewfile"'
alias brew_bundle_dump='brew bundle dump --force --file="$GITHUB/arwhyte/dotfiles-m1/brew/Brewfile"'

# pip (use active interpreter, uv-friendly)
alias pip_update='python -m pip freeze --user | cut -d= -f1 | xargs -n1 python -m pip install -U'
alias pip_update_venv='python -m pip freeze | cut -d= -f1 | xargs -n1 python -m pip install -U'

# Navigation
alias dev='cd "$DEV"'
alias docs='cd "$DOCS"'
alias dbx='cd "$DROPBOX"'
alias pics='cd "$PICS"'
alias github='cd "$GITHUB"'

alias arwhyte='cd "$ARWHYTE"'
alias dotfiles='cd "$ARWHYTE/dotfiles-m1"'
alias scripts='cd "$ARWHYTE/scripts"'

alias csev='cd "$CSEV"'
alias tsugi='cd "$CSEV/tsugiproject"'

alias umsi='cd "$UMSI"'
alias si506='cd "$UMSI/SI506"'
alias si506-metrics='cd "$UMSI/SI506-metrics"'
alias si506-site='cd "$UMSI/SI506-site"'
alias si664='cd "$UMSI/SI664"'
alias siads593='cd "$UMSI/SIADS593"'
alias siads593-site='cd "$UMSI/SIADS593-site"'
alias siads611='cd "$UMSI/SIADS611"'

# zsh helpers
alias ohmyzsh='cd "$HOME/.oh-my-zsh"'


# OLD .aliases content below (for reference)

# # DIRECTORY PATHS
# # HOME="/Users/arwhyte"  # REDUNDANT
# DEV="${HOME}/Development"
# DOCS="${HOME}/Documents"
# DROPBOX="${HOME}/Library/CloudStorage/Dropbox-Personal"
# PICS="${HOME}/Pictures"

# GITHUB="${DEV}/github"
# ARWHYTE="${GITHUB}/arwhyte"
# CSEV="${GITHUB}/csev"
# UMSI="${GITHUB}/umsi-arwhyte"

# # COMMANDS
# # See https://dougie.io/answers/pip-update-all-packages/
# alias brew_bundle_install="brew bundle install --file=${GITHUB}/arwhyte/dotfiles-m1/brew/Brewfile"
# alias brew_bundle_dump="brew bundle dump --force --file=${GITHUB}/arwhyte/dotfiles-m1/brew/Brewfile"

# # mypy
# alias mypy_umpyutl="mypy --python-executable \
#       ${HOME}/.pyenv/versions/3.12.2/envs/umpyutl_env/bin/python ${UMSI}/umpyutl/src/umpyutl \
#       --warn-redundant-casts --warn-return-any --warn-unreachable --warn-unused-ignores \
#       --show-absolute-path --show-error-codes --show-error-context --pretty"

# # pip (uv-friendly)
# alias pip_update='python -m pip freeze --user | cut -d= -f1 | xargs -n1 python -m pip install -U'
# alias pip_update_venv='python -m pip freeze | cut -d= -f1 | xargs -n1 python -m pip install -U'
# # alias pip_update="python3 -m pip freeze --user | cut -d'=' -f1 | xargs -n1 python3 -m pip install -U"
# # alias pip_update_venv="python3 -m pip freeze | cut -d'=' -f1 | xargs -n1 python3 -m pip install -U"

# # NAVIGATION
# alias dev="cd $DEV"
# alias docs="cd $DOCS"
# alias dbx="cd $DROPBOX"
# alias github="cd ${GITHUB}"
# alias pics="cd $PICS"

# alias arwhyte="cd ${ARWHYTE}"
# alias dotfiles="cd ${ARWHYTE}/dotfiles-m1"
# alias scripts="cd ${ARWHYTE}/scripts"

# alias csev="cd ${CSEV}"
# alias tsugi="cd ${CSEV}/tsugiproject"

# alias umsi="cd ${UMSI}"
# alias si506="cd ${UMSI}/SI506"
# alias si506-metrics="cd ${UMSI}/SI506-metrics"
# alias si506-site="cd ${UMSI}/SI506-site"
# alias si664="cd ${UMSI}/SI664"
# alias siads593="cd ${UMSI}/SIADS593"
# alias siads593-site="cd ${UMSI}/SIADS593-site"
# alias siads611="cd ${UMSI}/SIADS611"

# # zsh
# alias ohmyzsh='cd ${HOME}/.oh-my-zsh'

# # SWITCHES

# # alias ls='ls -laGH'
# # alias ls="/bin/ls -la"
