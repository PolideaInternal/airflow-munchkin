super().__init__(
    {% for var_name in args -%}
        {{ var_name }}{% if not loop.last %}, {% endif %}
    {% endfor %}
    {% if args and kwargs %}, {% endif %}
    {% for param_name, var_name in kwargs.items() -%}
        {{ param_name }}={{ var_name }}{% if not loop.last %}, {% endif %}
    {% endfor %}
)
