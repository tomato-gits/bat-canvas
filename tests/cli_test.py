from unittest import TestCase

import subprocess


class TestCli(TestCase):
    def test_hello(t):
        # run CLI command
        result = subprocess.run(["bat", "hello"], stdout=subprocess.PIPE)
        ret = result.stdout.decode("utf-8")
        t.assertEqual(ret, "Hello World!\n")

    def test_check_assignment(t):
        result = subprocess.run(["bat", "check_assignment"], stdout=subprocess.PIPE)
        ret = result.stdout.decode("utf-8")
        t.assertEqual(ret, "Assignment exists\n")