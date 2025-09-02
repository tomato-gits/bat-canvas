from unittest import TestCase

import subprocess


class TestCli(TestCase):
    def test_hello(t):
        # run CLI command
        result = subprocess.run(["bat", "hello"], stdout=subprocess.PIPE)
        ret = result.stdout.decode("utf-8")
        t.assertEqual(ret, "Hello World!\n")

    def test_check_assignment(t):
        token = "somestring"
        course_id = 1125693
        assignment_id = 6912376
        result = subprocess.run(["bat", "check_assignment", f"--token={token}", f"--courseid={course_id}", f"--assignmentid={assignment_id}"], stdout=subprocess.PIPE)
        ret = result.stdout.decode("utf-8")
        t.assertEqual(ret, "Assignment exists\n")