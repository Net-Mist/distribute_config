import argparse
import os
from unittest import TestCase, mock

from distribute_config import Config


class TestConfig(TestCase):
    def test_define_int(self):
        Config.clear()
        # int and flat float can be assign as int
        Config.define_int("test_int", 5, "A test for int")
        Config.define_int("test_int_float_valid", 5., "A test for int with a float var")

        # But not float
        with self.assertRaises(TypeError):
            Config.define_int("test_int_float_not_valid", 5.5, "A test for int with a float var")

        # Can't assign twice the same variable
        with self.assertRaises(KeyError):
            Config.define_int("test_int", 5, "A test for int")

        self.assertDictEqual(Config.get_dict(), {'test_int': 5, 'test_int_float_valid': 5})

    def test_namespace(self):
        Config.clear()
        Config.define_int("namespace1.test_int", 5, "A test for int")
        with Config.namespace("namespace2"):
            Config.define_int("test_int", 5, "A test for int")
            Config.define_int("subnamespace.test_int", 5, "A test for int")

            with Config.namespace("subnamespace2"):
                Config.define_int("plop", 4, "test of subnamespace")

        # print(Config.get_dict())
        self.assertDictEqual(Config.get_dict(), {'namespace1': {'test_int': 5},
                                                 'namespace2': {'test_int': 5, 'subnamespace': {'test_int': 5}, 'subnamespace2': {'plop': 4}}})

    def test_int(self):
        print(Config.get_dict())

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(v1=2, v2=3, c="conf.yml"))
    def test_load_conf(self, mock_args):
        Config.clear()
        Config.define_int("v1", 1, "var")
        Config.define_int("v2", 2, "var")
        Config.load_conf()
        self.assertEqual(Config.get_var("v1"), 2)
        self.assertEqual(Config.get_var("v2"), 3)

    @mock.patch.dict(os.environ, {"V1": "1", "NM__V2": "2"})
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(c="conf2.yml"))
    def test_load_conf_2(self, mock_args):
        Config.clear()
        Config.define_int("v1", 0, "var")
        Config.define_int("nm.v2", 0, "var")
        Config.load_conf()
        self.assertEqual(Config.get_var("v1"), 1)
        self.assertEqual(Config.get_var("nm.v2"), 2)
