#!/usr/bin/env bash

set -euo pipefail

# Ask if install Google Cloud SDK
echo "Install Google Cloud SDK [y/N]"
read install_gcloud

if [[ "${install_gcloud}" == "y" ]]; then
  curl https://sdk.cloud.google.com/ | bash -
fi
echo ""

# Setup project id
echo "Setup project id? [y/N]"
read setup_project_id
if [[ "${setup_project_id}" == "y" ]]; then
  export GCP_CONFIG_DIR=/config
  echo "Provide id of your Google Cloud Platform project:"
  read project_id
  export GCP_PROJECT_ID="${project_id}"
  gcloud auth login
  gcloud config set project "${project_id}"
fi
echo ""

# Create service key
echo "Create new key for account? [y/N]"
read create_new_key
if [[ "${create_new_key}" == "y" ]]; then
  echo "Provide name of service account you want to use ex. test-account"
  read account_name
  gcloud iam service-accounts keys create --iam-account "${account_name}@${project_id}.iam.gserviceaccount.com" /config/keys/sa.json
  gcloud auth activate-service-account --key-file=/config/keys/sa.json
fi
echo ""

# Create specific key
echo "Do you want to create key with specific name like my_key.json? [y/N]"
read create_key
if [[ "${create_key}" == "y" ]]; then
  echo "What should be the name? It should not contain .json"
  read key_name
  cp "/config/keys/sa.json" "/config/keys/${key_name}.json"
fi

set -x

export AIRFLOW_HOME=/opt/airflow
export AIRFLOW_CONFIG=/opt/airflow/tests/contrib/operators/postgres_local_executor.cfg
export GOOGLE_APPLICATION_CREDENTIALS=/config/keys/sa.json
export AIRFLOW__CORE__DAGS_FOLDER=$PWD/airflow/gcp/example_dags/
export AIRFLOW__CORE__LOAD_EXAMPLES=False
