{% for single_import in import_statement %}
from {{ single_import | to_package_name }} import {{ single_import | to_class_name }}
{% endfor %}

{% for class_block in class_blocks -%}
    {{ class_block }}
{% endfor %}
