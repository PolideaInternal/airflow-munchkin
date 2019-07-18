#!/bin/bash

# Create a issues related in repository.
#
# This script should be run from the project directory in which the issue is to be created.
#
# This file required the file with list of operators
#
# AIRFLOW-4966;Cloud AutoML NL Classification;https://cloud.google.com/natural-language/automl/docs/;https://googleapis.github.io/google-cloud-python/latest/automl/index.html
# AIRFLOW-4967;Cloud AutoML NL Entity Extraction;https://cloud.google.com/natural-language/automl/entity-analysis/docs/;https://googleapis.github.io/google-cloud-python/latest/automl/index.html
# AIRFLOW-4968;Cloud AutoML NL Sentiment; https://cloud.google.com/natural-language/automl/sentiment/docs/;https://googleapis.github.io/google-cloud-python/latest/automl/index.html
# AIRFLOW-4969;Cloud AutoML Tables;https://cloud.google.com/automl-tables/docs/;https://googleapis.github.io/google-cloud-python/latest/automl/index.html
# AIRFLOW-4970;Google Campaign Manager;https://developers.google.com/doubleclick-advertisers/;https://github.com/googleapis/google-api-python-client
# AIRFLOW-4971;Google Display & Video 360;https://developers.google.com/bid-manager/guides/getting-started-api;https://developers.google.com/bid-manager/guides/getting-started-api
# AIRFLOW-4972;Google Search Ads 360;https://developers.google.com/search-ads/;https://developers.google.com/resources/api-libraries/documentation/dfareporting/v3.3/python/latest/
# AIRFLOW-4973;Cloud Data Fusion Pipeline;https://cloud.google.com/data-fusion/docs/;https://developers.google.com/apis-explorer/#search/data%20fusion/datafusion/v1beta1/
#
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


while read line;do
    JIRA_TICKET=$(echo "${line}" | cut -d "[" -f 2 | cut -d "]" -f 1)
    TITLE=$(echo "${line}" | cut -d ";" -f 2)
    DOCS_LINK=$(gecho "${line}" | cut -d ";" -f 3)
    API_LINK=$(echo "${line}" | cut -d ";" -f 4)
    echo "Add ${TITLE} integration

Hi

Airflow lacks integration with the ${TITLE} service. I would be happy if Airflow had proper operators and hooks that integrate with this service.

Product Documentation: ${DOCS_LINK}
API Documentation: ${API_LINK}
Jira Ticket: https://issues.apache.org/jira/browse/${JIRA_TICKET}

$(test $(($RANDOM % 2)) -eq 0 && echo 'Lots of love' || echo 'Love')" | hub issue create -l OPERATORS -F -
done < "${1}"
