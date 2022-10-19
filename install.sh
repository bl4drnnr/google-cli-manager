#!/usr/bin/env bash

repository="https://github.com/bl4drnnr/google-cli-manager.git"

echo "Google Manager CLI installation..."

cd "$HOME"
mkdir -p "$HOME/.gmcli"
cd "$HOME/.gmcli"

git clone "$repository"

cd "$HOME/.gmcli/google-cli-manager"

for EACH_PROFILE in ".profile" ".bashrc" ".bash_profile" ".zprofile" ".zshrc"
    do
      echo "alias gmcli='python3 ${HOME}/.gmcli/google-cli-manager/main.py'" >> "${HOME}/${EACH_PROFILE}"
    done

/usr/bin/pip3 install -r "$HOME/.gmcli/google-cli-manager/requirements.txt"

echo "Google Manager CLI have been successfully installed..."