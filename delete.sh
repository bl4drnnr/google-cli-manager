#!/usr/bin/env bash

rm -r "$HOME/.gmcli"
path_to_purge="alias gmcli='python3 ${HOME}/.gmcli/google-cli-manager/main.py'"

for EACH_PROFILE in ".profile" ".bashrc" ".bash_profile" ".zprofile" ".zshrc"
  do
    sed -i "/${path_to_purge}/d" ~/${EACH_PROFILE}
  done

echo "Google Manager CLI has been successfully deleted successfully..."

