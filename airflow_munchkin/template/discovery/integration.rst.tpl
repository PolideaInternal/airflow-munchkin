{{ integration.service_name }}
'''''''''

{% for op in operators %}
:class:`airflow.gcp.operators.{{ integration.package_name }}.{{ op.class_name }}`
    {{ op.description | wrap_text(106) }}

{% endfor %}

They also use :class:`airflow.gcp.hooks.{{ integration.package_name }}.{{ operators[0].hook_class }}` to communicate with Google Cloud Platform.
