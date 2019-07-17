#!/bin/bash

hub issue -l JIRA -f "%t@%as%n" --state=all | sort|tee /dev/tty |cut -d "@" -f 2 | pbcopy
