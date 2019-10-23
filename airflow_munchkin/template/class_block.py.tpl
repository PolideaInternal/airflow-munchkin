class {{ name }}({{ extend_class | to_class_name }}):
{% filter indent(4, True) %}
{% if ctor_method %}
"""
{{ ctor_method.desc | wrap_text(106) }}

{% for arg in ctor_method_desc_args %}
{{ rst_param(arg.name, arg.desc, 106) }}
{% if arg.kind -%}
    :type {{ arg.name }}: {{ arg.kind.long_form  }}
{% endif %}
{% endfor %}
"""
{% endif %}
{% if method_blocks %}
{% for block in method_blocks -%}
    {{ block }}
{% endfor %}
{% else %}
pass
{% endif %}
{% endfilter %}
