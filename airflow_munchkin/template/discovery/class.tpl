class {{ operator.class_name }}(BaseOperator):
{% filter indent(4, True) %}
"""
{{ operator.description | wrap_text(106) }}

.. seealso::
    For more information on how to use this operator, take a look at the guide:
    :ref:`howto/operator:{{ operator.class_name }}`

{% for param in operator.params %}
{{ rst_param(param.pythonic_name, param.desc, 106) }}
{% if param.kind -%}
    :type {{ param.pythonic_name }}: {{ param.kind }}
{% endif %}
{% endfor %}

"""
template_fields = ({% for field in operator.template_fields %}"{{ field }}", {% endfor %})

google_api_service_name = "{{ operator.google_api_service_name }}"
google_api_endpoint_path = "{{ operator.google_api_endpoint_path }}"

{% include 'code_blocks/decorator_apply_defaults.py.tpl' %}

def __init__(
{% filter indent(4, True) %}
self,
{% for param in operator.params %}
{{ param.pythonic_name }}: {{ param.kind }}{% if not param.required %} = {{ param.default | python }}{% endif %},
{% endfor %}
*args,
**kwargs
{% endfilter %}
):
{% filter indent(4, True) %}
super().__init__(*args, **kwargs)
{% for param in operator.params %}
self.{{ param.pythonic_name }} = {{ param.pythonic_name }}
{% endfor %}
self.data = {
{% filter indent(4, True) %}
{% for param in operator.data_params %}
"{{ param.name }}": {{ param.pythonic_name }},
{% endfor %}
{% endfilter %}
}
{% endfilter %}

def execute(self, context):
{% filter indent(4, True) %}
hook = GoogleDiscoveryApiHook(
    gcp_conn_id=self.gcp_conn_id,
    delegate_to=self.delegate_to,
    api_service_name=self.google_api_service_name,
    api_version=self.api_version,
)
response = hook.query(endpoint=self.google_api_endpoint_path, data=self.data)
return response
{% endfilter %}
{% endfilter %}
