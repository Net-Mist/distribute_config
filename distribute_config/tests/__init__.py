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

        print(Config.get_dict())

    def test_int(self):
        print(Config.get_dict())
