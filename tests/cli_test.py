from unittest import TestCase

import subprocess


class TestCli(TestCase):
    def test_hello(t):
        # run CLI command
        result = subprocess.run(["bat", "hello"], stdout=subprocess.PIPE)
        ret = result.stdout.decode("utf-8")
        t.assertEqual(ret, "Hello World!\n")

    def test_check_assignment(t):
        config_file = 'config.yml'
        config_env = 'test'
        # token = "not_a_valid_token"
        course_id = 1125693
        assignment_id = 6912376
        result = subprocess.run([
            "bat",
            f"--config_file={config_file}",
            f"--config_env={config_env}",
            "check_assignment",
            # f"--token={token}",
            f"--courseid={course_id}",
            f"--assignmentid={assignment_id}",
        ], stdout=subprocess.PIPE)
        ret = result.stdout.decode("utf-8")
        t.assertEqual(ret, "Unauthorized error\n")