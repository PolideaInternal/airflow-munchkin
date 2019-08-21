{% include 'discovery/license.tpl' %}

"""
Example Airflow DAG that shows how to use {{ integration.service_name }}.
"""

from airflow.utils import dates
from airflow import models
from airflow.gcp.operators.{{ integration.package_name }} import ({% for op in operators %}{{ op.class_name }}, {% endfor %})

# [START howto_{{ integration.package_name }}_env_variables]
# TODO
# [END howto_{{ integration.package_name }}_env_variables]

default_args = {"start_date": dates.days_ago(1)}

with models.DAG(
    "example_{{ integration.package_name }}", default_args=default_args, schedule_interval=None  # Override to match your needs
) as dag:
{% filter indent(4, True) %}
{% for ex in examples %}
{{ ex }}

{% endfor %}
{% endfilter %}
