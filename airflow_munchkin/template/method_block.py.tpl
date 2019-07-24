{% macro arguments_list(arguments) -%}
    {% for name, info in arguments.items() -%}
        {{ name }}:
        {% if info.kind.is_optional -%}
            {{ info.kind.indexes[0].short_form }} = None
        {% else %}
            {{ info.kind.short_form }}
        {% endif %}
        {% if not loop.last -%}, {% endif %}
    {% endfor %}
{% endmacro %}

def {{ name }}(self, {{ arguments_list(args) }}):
{# TODO: Implement return_kind#}
{#-> {{ return_kind }}:#}
{% if desc %}
{% filter indent(4, true) -%}
"""
{{ desc | wrap_text(102) }}

{% for arg in args.values() %}
{{ rst_param(arg.name, arg.desc, 102) }}
:type {{ arg.name }}: {{ arg.kind.long_form  }}
{% endfor %}
"""
{% endfilter %}
{% endif %}
{% filter indent(4, true) -%}
{% if code_blocks %}
{% for block in code_blocks -%}
    {{ block }}
{% endfor %}
{% else %}
pass
{% endif %}
{% endfilter %}
