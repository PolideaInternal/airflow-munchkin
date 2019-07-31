with self.assertRaises(AirflowException):
{% filter indent(4, true) %}
    {% include "code_blocks/method_call.py.tpl" %}
{% endfilter %}
