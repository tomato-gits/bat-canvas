from unittest import TestCase
from unittest.mock import patch, Mock
from bat.lib import hello_world, check_assignment, check_assignment_cfg

SRC = 'bat.lib'

class LibTests(TestCase):

    def test_hello_world(t):
        ret = hello_world()
        t.assertEqual(ret, "Hello World!")

    @patch(f"{SRC}.get",autospec=True)
    def test_check_assignment(t, get:Mock):
        courseid = "+courseid+"
        assignmentid = "+assignmentid+"
        endpoint = f"https://utexas.instructure.com/api/v1/courses/{courseid}/assignments/{assignmentid}"
        token = "+token+"
        headers = {"Authorization": f"Bearer {token}"}

        with t.subTest("assignment exists"):
            get.return_value.status_code = 200
            ret = check_assignment(courseid=courseid, assignmentid=assignmentid, token=token)
            t.assertEqual(ret, "Assignment exists")
            get.assert_called_with(endpoint, headers=headers)

        get.reset_mock()

        with t.subTest("assignment does not exist"):
            get.return_value.status_code = 404
            ret = check_assignment(courseid=courseid, assignmentid=assignmentid, token=token)
            t.assertEqual(ret, "Assignment does not exist")
            get.assert_called_with(endpoint, headers=headers)

    # remember! patches get applied in reverse order
    @patch(f"{SRC}.check_assignment",autospec=True)
    @patch(f"{SRC}.get_config", autospec=True)
    def test_check_assignment_cfg(t, get_config:Mock, check_assignment:Mock):
        # mock get_config, test that it runs get_config without args, then calls check_assignment with params from config
        ret = check_assignment_cfg()

        cfg = get_config.return_value
        get_config.assert_called_with()
        check_assignment.assert_called_with(courseid=cfg.courseid, assignmentid=cfg.assignmentid, token=cfg.token)
        t.assertIs(ret, check_assignment.return_value)


class TempTests(TestCase):

    def test_class_property(t):

        class _Prop:
            def __get__(self, _, objtype):
                try:
                    return objtype._property
                except AttributeError:
                    objtype._property = objtype.get_property()
                return objtype._property

            def __set__(self, objtype, value):
                objtype._property = value

        class MetaClass:
            def __init_subclass__(cls, **kwargs):
                cls.prop = _Prop()

            @classmethod
            def get_property(cls):
                return "dynamical property value"

        class SubCls(MetaClass):
            _property = "subby prop"

        t.assertEqual(SubCls.prop, "subby prop")

        class DubSub(MetaClass):
            @classmethod
            def get_property(cls):
                return "dubsub property value"

        t.assertEqual(DubSub.prop, "dubsub property value")

        DubSub.prop = "new value"
        t.assertEqual(DubSub.prop, "new value")
