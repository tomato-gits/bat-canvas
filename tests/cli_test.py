from unittest import TestCase

import subprocess


class TestCli(TestCase):
    def test_hello(t):
        # run CLI command
        result = subprocess.run(["bat", "hello"], stdout=subprocess.PIPE)
        ret = results.stdout.decode("utf-8")
        t.assertEqual(ret, "wark")
