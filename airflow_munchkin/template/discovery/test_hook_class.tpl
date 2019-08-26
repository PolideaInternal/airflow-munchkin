@mock.patch("airflow.gcp.hooks.{{ package_name }}.{{ operator.hook_class }}.get_conn")
@mock.patch("airflow.gcp.hooks.{{ package_name }}.BaseOperator.__init__")
def test_{{ operator.method.name | snake }}(self, base_op_mock, get_conn_mock):
{% filter indent(4, True) %}
{% for param in operator.params %}
{% if param.pythonic_name not in ('api_version', 'gcp_conn_id', 'delegate_to') %}
{{ param.pythonic_name }} = {{  param.pythonic_name | test_constant(param.kind) | python }}
{% endif %}
{% endfor %}

return_value = "TEST"
get_conn_mock.return_value.{{ operator.resource_name }}.return_value.{{operator.method.name | snake }}.return_value.execute.return_value = return_value

result = self.hook.{{ operator.method.name | snake }}(
{% for param in operator.params %}
{% if param.pythonic_name not in ('api_version', 'gcp_conn_id', 'delegate_to') %}
{{ param.pythonic_name }} = {{  param.pythonic_name }},
{% endif %}
{% endfor %}
)

get_conn_mock.return_value.{{ operator.resource_name }}.return_value.{{operator.method.name | snake }}.assert_called_once_with(
{% for param in operator.params %}
{% if param.pythonic_name not in ('api_version', 'gcp_conn_id', 'delegate_to') %}
{{ param.name }}={{  param.pythonic_name }},
{% endif %}
{% endfor %}
)

self.assertEqual(return_value, result)

{% endfilter %}
