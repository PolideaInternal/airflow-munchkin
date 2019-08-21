..  Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at

..    http://www.apache.org/licenses/LICENSE-2.0

..  Unless required by applicable law or agreed to in writing,
    software distributed under the License is distributed on an
    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
    KIND, either express or implied.  See the License for the
    specific language governing permissions and limitations
    under the License.

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

.. exampleinclude:: ../../../../airflow/gxp/example_dags/example_{{ integration.package_name }}.py
    :language: python
    :dedent: 4
    :start-after: [START {{ op.class_name | howto }}]
    :end-before: [END {{ op.class_name | howto }}]

You can use :ref:`Jinja templating <jinja-templating>` with
:template-fields:`airflow.gcp.operators.{{ integration.package_name }}.{{ op.class_name }}`
parameters which allows you to dynamically determine values.
The result is saved to :ref:`XCom <concepts:xcom>`, which allows it to be used by other operators.

{% endfor %}
