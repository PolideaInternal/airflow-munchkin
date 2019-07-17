#!/bin/bash

hub issue -l JIRA -f "%t@%S%n" --state=all | sort | tee /dev/tty | cut -d "@" -f 2 | pbcopy
