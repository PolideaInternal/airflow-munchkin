class Test{{ operator.class_name }}(TestCase):
{% filter indent(4, True) %}
@mock.patch('airflow.gcp.operators.{{ file_name }}.GoogleDiscoveryApiHook', )
@mock.patch('airflow.gcp.operators.{{ file_name }}.BaseOperator', )
def test_execute(self, base_op_mock, discovery_hook_mock):
    {% for param in operator.params %}
    {% if param.pythonic_name not in ('api_version', 'gcp_conn_id', 'delegate_to') %}
    {{ param.pythonic_name }} = {{  param.pythonic_name | test_constant(param.kind) | python }}
    {% endif %}
    {% endfor %}
    api_service_name = {{ operator.google_api_service_name | python }}
    api_path_name = {{ operator.google_api_endpoint_path | python }}
    op = {{ operator.class_name }}(
        {% include "discovery/op_args.tpl" %}
        api_version=API_VERSION,
        task_id="test_task"
    )
    op.execute(context=None)
    discovery_hook_mock.assert_called_once_with(
        gcp_conn_id=GCP_CONN_ID,
        delegate_to=None,
        api_service_name=api_service_name,
        api_version=API_VERSION,
    )
    data = {
      {% filter indent(4, True) %}
      {% for param in operator.data_params %}
      "{{ param.name }}": {{ param.pythonic_name }},
      {% endfor %}
      {% endfilter %}
    }
    discovery_hook_mock.return_value.query.assert_called_once_with(
        endpoint=api_path_name, data=data
    )
{% endfilter %}
