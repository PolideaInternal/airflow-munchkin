class Test{{ operator.class_name }}(TestCase):
{% filter indent(4, True) %}
@mock.patch('airflow.gcp.operators.{{ package_name }}.{{ operator.hook_class }}', )
@mock.patch('airflow.gcp.operators.{{ package_name }}.BaseOperator', )
def test_execute(self, mock_base_op, hook_mock):
    {% for param in operator.params %}
    {% if param.pythonic_name not in ('api_version', 'gcp_conn_id', 'delegate_to') %}
    {{ param.pythonic_name }} = {{  param.pythonic_name | test_constant(param.kind) | python }}
    {% endif %}
    {% endfor %}
    op = {{ operator.class_name }}(
        {% include "discovery/op_args.tpl" %}
        api_version=API_VERSION,
        task_id="test_task"
    )
    op.execute(context=None)
    hook_mock.assert_called_once_with(
        gcp_conn_id=GCP_CONN_ID,
        delegate_to=None,
        api_version=API_VERSION,
    )
    hook_mock.return_value.{{ operator.method.name | snake }}.assert_called_once_with(
        {% for param in operator.params %}
        {% if param.pythonic_name not in ('api_version', 'gcp_conn_id', 'delegate_to') %}
        {{ param.pythonic_name }} = {{  param.pythonic_name }},
        {% endif %}
        {% endfor %}
    )
{% endfilter %}
