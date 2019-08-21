{% for param in operator.params %}
{% if param.pythonic_name not in ('api_version', 'gcp_conn_id', 'delegate_to') %}
{{ param.pythonic_name }}={{ param.pythonic_name }},
{% endif %}
{% endfor %}
