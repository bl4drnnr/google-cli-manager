#!/usr/bin/env bash

rm -r "$HOME/.gmcli"

for EACH_PROFILE in ".profile" ".bashrc" ".bash_profile" ".zprofile" ".zshrc"
  do
    sed -i '' -e '\|^alias gmcli|d' ~/${EACH_PROFILE}
  done

echo "Google Manager CLI has been successfully deleted successfully..."
