from unittest import TestCase, mock
from airflow.gcp.operators.{{ package_name }} import ({% for op in operators %}{{ op.class_name }}, {% endfor %})

API_VERSION = 'api_version'
GCP_CONN_ID = 'google_cloud_default'


{% for test in tests %}
{{ test }}

{% endfor %}
