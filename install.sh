#!/usr/bin/env bash

repository="https://github.com/bl4drnnr/google-cli-manager.git"

echo "Google-Manager CLI installation..."

cd "$HOME"
mkdir -p "$HOME/.gmcli"
cd "$HOME/.gmcli"

git clone "$repository"

cd "$HOME/github-cli-manager"

for EACH_PROFILE in ".profile" ".bashrc" ".bash_profile" ".zprofile" ".zshrc"
    do
      echo "alias gmcli='python3 ${HOME}/.gmcli/google-cli-manager/main.py'" >> "${HOME}/${EACH_PROFILE}"
    done

pip install -r "$HOME/.gmcli/requirements.txt"

echo "Google-Manager CLI have been successfully installed..."
