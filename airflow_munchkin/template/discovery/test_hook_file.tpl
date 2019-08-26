{% include 'discovery/license.tpl' %}

from unittest import TestCase, mock
from airflow.gcp.hooks.{{ package_name }} import {{ hook_class }}
from tests.contrib.utils.base_gcp_mock import mock_base_gcp_hook_default_project_id

API_VERSION = {{ integration.version | python }}
GCP_CONN_ID = 'google_cloud_default'

class Test{{ hook_class }}(TestCase):
{% filter indent(4, True) %}
def setUp(self):
    with mock.patch(
        "airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook.__init__",
        new=mock_base_gcp_hook_default_project_id,
    ):
        self.hook = {{ hook_class }}(gcp_conn_id=GCP_CONN_ID)

{% for test in tests %}
{{ test }}

{% endfor %}
{% endfilter %}
