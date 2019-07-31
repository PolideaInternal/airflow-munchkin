@mock.patch(  # type: ignore
    "airflow.contrib.hooks.{{ file_block.file_name }}.{{ class_block.name }}.get_conn",
    {% if return_value %}
    **{
        "return_value.{{ method_name }}.return_value": {{ return_value }}
    },  # type: ignore
    {% endif %}
)
