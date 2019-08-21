{% include 'discovery/license.tpl' %}

"""
This module contains {{ integration.service_name  }} operators.
"""
from typing import Tuple, List, Any, Dict, Optional

from airflow.utils.decorators import apply_defaults
from airflow.models.baseoperator import BaseOperator
from airflow.contrib.hooks.google_discovery_api_hook import GoogleDiscoveryApiHook


{% for op in operators %}
{{ op }}

{% endfor %}
