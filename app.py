from distribute_config import Config, ConfigNamespace

Config.define_int("bs", 5, "Batch size to train the model")
Config.define_int("test.bs", 5, "Batch size to test the model")

with ConfigNamespace("plop"):
    Config.define_int("bs", 5, "Batch size to train the model")


Config.load_conf()
