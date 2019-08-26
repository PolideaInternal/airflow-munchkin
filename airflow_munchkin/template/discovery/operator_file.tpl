{% include 'discovery/license.tpl' %}

"""
This module contains Google {{ integration.service_name  }} operators.
"""
from typing import Tuple, List, Any, Dict, Optional

from airflow.utils.decorators import apply_defaults
from airflow.models.baseoperator import BaseOperator
from airflow.gcp.hooks.{{ integration.package_name }} import {{ hook_class }}


{% for op in operators %}
{{ op }}

{% endfor %}
