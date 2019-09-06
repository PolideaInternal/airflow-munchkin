import unittest
from tests.contrib.utils.base_gcp_system_test_case import SKIP_TEST_WARNING, DagGcpSystemTestCase
from tests.contrib.utils.gcp_authenticator import {{ key }}


@unittest.skipIf(DagGcpSystemTestCase.skip_check({{ key }}), SKIP_TEST_WARNING)
class {{ integration.service_name }}SystemTest(DagGcpSystemTestCase):
    def __init__(self, method_name="runTest"):
        super().__init__(
            method_name, dag_id="example_{{ integration.package_name }}", gcp_key={{ key }}
        )

    def test_run_example_dag(self):
        self._run_dag()
