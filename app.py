from distribute_config import Config

Config.define_int("bs", 5, "Batch size to train the model")
Config.define_int("test.bs", 5, "Batch size to test the model")


Config.load_conf()
