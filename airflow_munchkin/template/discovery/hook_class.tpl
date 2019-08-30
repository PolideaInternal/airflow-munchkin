"""
This module contains Google {{ integration.service_name  }} hook.
"""
from typing import Tuple, List, Any, Dict, Optional

from googleapiclient.discovery import build

from airflow.contrib.hooks.gcp_api_base_hook import GoogleCloudBaseHook

class {{ integration.service_name  }}Hook(GoogleCloudBaseHook):
{% filter indent(4, True) %}
"""
Hook for Google {{ integration.service_name }}.
"""
_conn = None  # type: Optional[Any]

def __init__(
{% filter indent(4, True) %}
self,
api_version: str = {{ integration.version | python }},
gcp_conn_id: str = 'google_cloud_default',
delegate_to: str = None) -> None:
super().__init__(gcp_conn_id, delegate_to)
self.api_version = api_version
{% endfilter %}

def get_conn(self):
{% filter indent(4, True) %}
"""
Retrieves connection to {{ integration.service_name }}.
"""
if not self._conn:
    http_authorized = self._authorize()
    self._conn = build({{ endpoint.service | python }}, self.api_version,
                       http=http_authorized, cache_discovery=False)
return self._conn
{% endfilter %}

{% for m in methods %}
{{ m }}
{% endfor %}

{% endfilter %}
