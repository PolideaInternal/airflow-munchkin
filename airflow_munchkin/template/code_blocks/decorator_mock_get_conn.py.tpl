@mock.patch(  # type: ignore
    "{{ class_path }}.get_conn",
    {% if return_value is defined and return_value %}
    **{
        "return_value.{{ method_name }}.return_value": {{ return_value }}
    },  # type: ignore
    {% endif %}
)
