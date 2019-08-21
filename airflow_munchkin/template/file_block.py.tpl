{% for single_import in import_statement %}
from {{ single_import | to_package_name }} import {{ single_import | to_class_name }}
{% endfor %}

{% if constants %}
    {% for constant in constants -%}
        {{ constant.name }}{% if constant.kind %}: {{ constant.kind.short_form }}{% endif %}= {{ constant.value }}
    {% endfor %}
{% endif %}
{% for class_block in class_blocks -%}
    {{ class_block }}
{% endfor %}
