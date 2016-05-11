#!/bin/bash

# Creates a virtual device on IBM SoftLayer

set -e

# Require the SoftLayer CLI
command -v slcli virtual create --help >/dev/null 2>&1 ||
  {
    echo >&2 "SoftLayer CLI not installed.  Run 'pip install SoftLayer' first.";
    exit 1;
  }

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

slcli -y virtual create \
  --template "$DIR/vm.template" \
  "$@"
