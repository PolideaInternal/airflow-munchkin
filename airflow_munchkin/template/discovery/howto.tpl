Google {{ integration.service_name}} Operators
=======================================

Here goes a copy pasted text from service website.

.. contents::
  :depth: 1
  :local:

Prerequisite Tasks
^^^^^^^^^^^^^^^^^^

.. include:: _partials/prerequisite_tasks.rst

{% for op in operators %}
.. _howto/operator:{{ op.class_name }}:

A section title
^^^^^^^^^^^^^^^

Here describe how to use :class:`~airflow.gcp.operators.{{ integration.package_name }}.{{ op.class_name }}`.

.. exampleinclude:: ../../../../airflow/gcp/example_dags/example_{{ integration.package_name }}.py
    :language: python
    :dedent: 4
    :start-after: [START {{ op.class_name | howto }}]
    :end-before: [END {{ op.class_name | howto }}]

You can use :ref:`Jinja templating <jinja-templating>` with
:template-fields:`airflow.gcp.operators.{{ integration.package_name }}.{{ op.class_name }}`
parameters which allows you to dynamically determine values.
The result is saved to :ref:`XCom <concepts:xcom>`, which allows it to be used by other operators.

{% endfor %}
