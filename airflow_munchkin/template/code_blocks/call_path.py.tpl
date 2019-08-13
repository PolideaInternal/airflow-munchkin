{{ var_name }} = {{ client.name }}.{{ fn_name }}(
    {% for arg_name in args -%}
        {{ arg_name }}{% if not loop.last %}, {% endif %}
    {% endfor %}
)
