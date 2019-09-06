def {{ operator.method.name | snake }}(
{% filter indent(4, True) %}
self,
{% for param in operator.params %}
{% if param.pythonic_name not in ('api_version', 'gcp_conn_id', 'delegate_to') %}
{{ param.pythonic_name }}: {{ param.kind }}{% if not param.required %} = {{ param.default | python }}{% endif %},
{% endif %}
{% endfor %}
{% endfilter %}
) -> Any:
{% filter indent(4, True) %}
"""
{{ operator.description | wrap_text(106) }}

{% for param in operator.params %}
{% if param.pythonic_name not in ('api_version', 'gcp_conn_id', 'delegate_to') %}
{{ rst_param(param.pythonic_name, param.desc, 106) }}
{% if param.kind -%}
    :type {{ param.pythonic_name }}: {{ param.kind }}
{% endif %}
{% endif %}
{% endfor %}
"""
response = self.get_conn().{{ operator.resource_name }}().{{ operator.method.name }}(  # pylint: disable=no-member
{% filter indent(4, True) %}
{% for param in operator.params %}
{% if param.pythonic_name not in ('api_version', 'gcp_conn_id', 'delegate_to') %}
{{ param.name }}={{ param.pythonic_name }},
{% endif %}
{% endfor %}
{% endfilter %}
).execute(num_retries=self.num_retries)
return response
{% endfilter %}
