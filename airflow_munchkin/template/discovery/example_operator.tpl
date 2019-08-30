# [START {{ operator.class_name | howto }}]
{{ operator.class_name | snake }}_task = {{ operator.class_name }}(
    {% for param in operator.params %}
    {% if param.required %}
    {{ param.pythonic_name }}={{ param.pythonic_name }},
    {% endif %}
    {% endfor %}
    task_id="{{ operator.class_name | snake }}_task",
)
# [END {{ operator.class_name | howto }}]
