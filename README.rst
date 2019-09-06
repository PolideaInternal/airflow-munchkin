================
Airflow Munchkin
================


.. image:: https://img.shields.io/pypi/v/airflow_munchkin.svg
        :target: https://pypi.python.org/pypi/airflow_munchkin

.. image:: https://travis-ci.com/PolideaInternal/airflow-munchkin.svg?branch=master
        :target: https://travis-ci.com/PolideaInternal/airflow-munchkin

.. image:: https://readthedocs.org/projects/airflow-munchkin/badge/?version=latest
        :target: https://airflow-munchkin.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/PolideaInternal/airflow_munchkin/shield.svg
     :target: https://pyup.io/repos/github/PolideaInternal/airflow_munchkin/
     :alt: Updates



Airflow Munchkin is a simple code generator that improves first stages of developing
`Airflow <https://github.com/apache/airflow>`_ operators for Google services including
Google Cloud Platform and Marketing Platform. Moreover we like cats, thus this name.


* Free software: MIT license
* Documentation: https://airflow-munchkin.readthedocs.io.


What Munchkin does?
-------------------
Munchkin is a code generator that helps developers to scaffold operators and hooks.
By using Munchkin you will get:

- hook class (including method descriptions, arguments types etc.)

- operators classes (including descriptions, arguments types and execute method)

- base unit tests for both, hook and operators

- example DAG with links to how to guide

- skeleton of howto.rst that should include information how end user can use the operators

- short information that should be added to ``airflow.docs.integration.rst``

- skeleton of system test for operators

In other words, you get everything that can be seen as a "boring work".

What Munchkin does not?
-----------------------
Munchkin does not perform the interesting part of implementing an operator which includes:

- making operators idempotent

- handling exceptions

- converting an operator to a sensor (if required)

- adding nice how-to information

How to use Munchkin
-------------------
It's very simple. Here is a step by step guide:

- Select a Google service

- Determine if the service has a Python client (you can check it `here <https://google-cloud.readthedocs.io/en/latest/index.html>`_)

- If a client exist and it has a method you want to use then you should use `Munchkin for client`_

- If there's no Python client then the operators will be based on the `Discovery API <https://developers.google.com/discovery/>`_ - in this case you have to determine the API endpoint using `the explorer <https://developers.google.com/apis-explorer/#p/>`_. If you can't find the service, use Google to find `myService API` to determine the path used in REST requests. Finally use `Munchkin for discovery`_.

.. _Munchkin for client:

Munchkin for Google Cloud libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Generator for Python clients is located under ``airflow_munchkin.main_client``. To use it you have to modify
the Integration information in `main` function:

.. code-block:: python

    integration_info: Integration = Integration(
        service_name="Cloud Memorystore",
        class_prefix="CloudMemorystore",
        file_prefix="gcp_cloud_memorystore",
        client_path="google.cloud.redis_v1.CloudRedisClient",
    )

The most important part of the integration is ``client_path`` which indicates the 'client' object. Additionally
you can define class and file prefixes and service name.

.. _Munchkin for discovery:

Munchkin for Google APIs Python Client
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Generator for Discovery API is located under ``airflow_munchkin.main_discovery``. To use it you have to modify
the Integration information in ``main`` function:

.. code-block:: python

    integration = DiscoveryIntegration(
        api_path="doubleclickbidmanager.queries",
        version="v1",
        methods=None,
        service_name="DisplayVideo",
        object_name="Report",
        class_prefix="Google",
        package_name=resolve_package_name(service_name),
    )

The most important part of the integration is ``api_path`` which indicates the API endpoint. It could be
full path to a resource (ex. ``dfareporting.campaigns``) or to a single method (ex. ``dfareporting.campaigns.insert``).
You also have to provide valid ``api_version``.

If you use the path for a resource then you can specify for which methods operators should be generated
(ex. ``methods=['get', 'list']``). Otherwise all methods will be parsed. Additionally you can specify ``service_name``,
``class_prefix`` and ``object_name``. Object name is used to obtain better operators class names and it's added after method
name (ex. ServiceNameMethodOBJECTOperator, DisplayVideoGetReportOperator).

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
