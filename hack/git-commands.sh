#!/bin/bash

# Sends the last commit to pastebin and creates a command to add the commit to local repository.
# In next step, displays it on terminal and copies it to the clipboard.
alias send_last_commit='echo curl $(git format-patch -k --stdout HEAD^..HEAD | nc termbin.com 9999) \| git am | tee /dev/tty | pbcopy'

function pr_fetch() {
  # Fetch changes from PR, but does not create branch.
  # Useful for making review.
  if [ $# -eq 1 ]; then
    REMOTE_NAME="origin"
    PULL_REQUEST_NO=$1
  elif [ $# -eq 2 ]; then
    REMOTE_NAME=$1
    PULL_REQUEST_NO=$2
  else
    echo "You must provide a PR number"
    return
  fi
  git fetch "${REMOTE_NAME}" "+refs/pull/${PULL_REQUEST_NO}/merge:"
  git checkout -qf FETCH_HEAD
}
