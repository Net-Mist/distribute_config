from unittest import TestCase

from distribute_config import Config


class TestConfig(TestCase):
    def test_define(self):
        # int and flat float can be assign as int
        Config.define_int("test_int", 5, "A test for int")
        Config.define_int("test_int_float_valid", 5., "A test for int with a float var")

        # But not float
        with self.assertRaises(TypeError):
            Config.define_int("test_int_float_not_valid", 5.5, "A test for int with a float var")

        # Can't assign twice the same variable
        with self.assertRaises(KeyError):
            Config.define_int("test_int", 5, "A test for int")

        # print(Config.get_dict())
        self.assertDictEqual(Config.get_dict(), {'test_int': 5, 'test_int_float_valid': 5})

    def test_namespace(self):
        Config.define_int("namespace1.test_int", 5, "A test for int")
        with Config.namespace("namespace2"):
            Config.define_int("test_int", 5, "A test for int")
            Config.define_int("subnamespace.test_int", 5, "A test for int")

            with Config.namespace("subnamespace2"):
                Config.define_int("plop", 4, "test of subnamespace")

        # print(Config.get_dict())
        self.assertDictEqual(Config.get_dict(), {'test_int': 5, 'test_int_float_valid': 5, 'namespace1': {'test_int': 5},
                                                 'namespace2': {'test_int': 5, 'subnamespace': {'test_int': 5}, 'subnamespace2': {'plop': 4}}})

    def test_int(self):
        print(Config.get_dict())
