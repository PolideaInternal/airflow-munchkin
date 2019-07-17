#!/bin/bash

set -Eeuo pipefail

if [ "$#" -lt 1 ]; then
	echo "You must provide a file name."
	exit 1
fi

if [ -z  "${1}" ]; then
	echo "You must provie a file name."
	exit 1
fi

if [ ! -e "${1}" ]; then
	echo "File not exists"	
	exit 1
fi

function jira {
	./jira.sh --server https://issues.apache.org/jira/ \
	    --user "${JIRA_USERNAME}" \
	    --password "${JIRA_PASSWORD}" $@
}

function getIssue {
	jira --action getIssue --issue "$1"
}

while read line;do 
	SUMMARY=$(getIssue "${line}" | grep Summary | cut -d ":" -f 2)
	echo "[${line}]${SUMMARY}"
done < "${1}"

